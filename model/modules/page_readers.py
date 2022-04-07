import requests
import validators
from bs4 import BeautifulSoup as soup
from urllib.parse import urlparse, urljoin


class BaseReader:
    def __init__(self, url, session_headers={'User-Agent': 'Mozilla/5.0'}):
        assert validators.url(url), "Invalid url."
        self.url = url
        self.status = 'unscraped'
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
        if not url:
            url = self.url
        response = self._get_response(url)
        if response.status_code == 200:
            return soup(response.text, "html.parser")



class MainPageReader(BaseReader):
    url = "https://www.gpuzoo.com/"
    def __init__(self, url=url):
        super().__init__(url)

    def read_gpu_category_urls(self, soup):
        gpu_category_urls = set()
        for a in soup.find_all('a', href=True):
            o = urlparse(a['href']).path
            if o.startswith('/GPU'):
                gpu_category_urls.add(urljoin(self.url, o))

        return gpu_category_urls

    def read(self):
        self.soup = self.parse_page()
        self.gpu_category_urls = self.read_gpu_category_urls(soup=self.soup)








