import requests
import validators
from bs4 import BeautifulSoup as soup
from urllib.parse import urlparse, urljoin
from typing import List
from tqdm.autonotebook import tqdm
import concurrent.futures
import logging
import traceback

logger = logging.getLogger(__name__)

class BaseReader:
    main_page_url = "https://videocardz.net/"
    def __init__(self, url=None, session_headers={'User-Agent': 'Mozilla/5.0'}):
        self.status = 'unscraped'
        self.url = url
        self.session_headers = session_headers
        self.session = self._make_session()

    def _make_session(self):
        s = requests.Session()
        s.headers.update(self.session_headers)
        return s

    def _get_response(self, url: str):
        """
        Gets HTTP response from url.
        :param url:
        """
        return self.session.get(url)

    def parse_page(self, url=None):
        """
        Parses a webpage with BeatifoulSoup.
        :param url:
        """
        response = self._get_response(url)
        if response.status_code == 200:
            return soup(response.text, "html.parser")


class GPUReader(BaseReader):
    def __init__(self, url):
        super().__init__(url)
        self.gpu_specification = None

    def _read_gpu_specification(self, soup):
        headers = soup.find_all(class_="title")
        gpu_specifications = dict.fromkeys([header.text for header in headers])
        for header in headers:
            value = header.find_next_siblings()[0].text.strip()
            gpu_specifications[header.text] = value
        return gpu_specifications

    def read(self):
        soup = self.parse_page(url=self.url)
        self.gpu_specification = self._read_gpu_specification(soup=soup)


class ManufacturerPageReader(BaseReader):
    def __init__(self, url):
        super().__init__(url)
        self.product_line_urls = set()

    def find_product_line_urls(self, soup):
        product_line_urls = set()
        tags = soup.find_all('div', class_='block5')
        for tag_list in tags:
            for a in tag_list.find_all('a', href=True):
                o = urlparse(a['href']).path
                product_line_urls.add(urljoin(self.url, o))

        return product_line_urls

    def find_product_urls_from_product_line_url(self, product_line_url):
        product_urls = set()
        soup = self.parse_page(product_line_url)
        for a in soup.find_all('a', href=True, ):
            if a.find('strong'):
                o = urlparse(a['href']).path
                product_urls.add(urljoin(self.main_page_url, o))

        return product_urls

    def find_all_product_urls(self, product_line_urls: List[str]):
        all_product_urls = set()
        with concurrent.futures.ThreadPoolExecutor(max_workers=32) as executor:
            future_to_url = {executor.submit(self.find_product_urls_from_product_line_url, url): url for url in self.product_line_urls}
            for future in tqdm(concurrent.futures.as_completed(future_to_url), total=len(product_line_urls)):
                url = future_to_url[future]
                try:
                    product_urls = future.result()
                    all_product_urls.update(product_urls)
                except Exception as e:
                    logger.critical(
                        f"Page at {url} returned an unhandled exception during scraping attempt. \n---TRACEBACK---\n"
                    )
                    traceback.print_exc()

        return all_product_urls

    def read(self):
        self.soup = self.parse_page(url=self.url)
        self.product_line_urls = self.find_product_line_urls(soup=self.soup)
        self.product_urls = self.find_all_product_urls(self.product_line_urls)

class MainPageReader(BaseReader):
    def __init__(self):
        super().__init__()
        self.gpu_category_urls = set()

    def split_and_merge(self, s, n_elements=3):
        return '/'.join(s.split('/')[:n_elements])

    def read_gpu_category_urls(self, soup):
        gpu_category_urls = set()
        for a in soup.find_all('a', href=True):
            o = urlparse(a['href']).path
            if o.startswith('/browse'):
                # Need to split and merge the url to keep just the category name.
                o = self.split_and_merge(s=o)
                gpu_category_urls.add(urljoin(self.main_page_url, o))

        return gpu_category_urls
    #     gpu_category_urls = set()
    #     for a in soup.find_all('a', href=True):
    #         o = urlparse(a['href']).path
    #         if o.startswith('/GPU') and o.endswith("index.html"):
    #             gpu_category_urls.add(urljoin(self.url, o))
    #
    #     return gpu_category_urls
    #
    def read(self):
        self.soup = self.parse_page(url=self.main_page_url)
        self.gpu_category_urls = self.read_gpu_category_urls(soup=self.soup)













