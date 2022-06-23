from typing import Dict

class GPU:
    def __init__(self, specification):
        if specification is not None:
            assert isinstance(specification, Dict), "Please provide a specification dictionary."
        self.manufacturer = GPUSpecification(name='manufacturer', raw_specification=specification.get('manufacturer'))
        self.original_series = GPUSpecification(
            name='original_series', raw_specification=specification.get('original_series')
        )
        self.release_date = GPUSpecification(name='release_date', raw_specification=specification.get('release_date'))
        self.pcb_code = GPUSpecification(name='pcb_code', raw_specification=specification.get('pcb_code'))
        self.p_n_code = GPUSpecification(name='p_n_code', raw_specification=specification.get('p_n_code'))
        self.model = GPUSpecification(name='model', raw_specification=specification.get('model'))
        self.gpu_model = GPUSpecification(name='gpu_model', raw_specification=specification.get('gpu_model'))
        self.architecture = GPUSpecification(name='architecture', raw_specification=specification.get('architecture'))
        self.fabrication_process = GPUSpecification(
            name='fabrication_process', raw_specification=specification.get('fabrication_process')
        )
        self.die_size = GPUSpecification(name='die_size', raw_specification=specification.get('die_size'))
        self.transistors_count = GPUSpecification(
            name='transistors_count', raw_specification=specification.get('transistors_count')
        )
        self.transistors_density = GPUSpecification(
            name='transistors_density', raw_specification=specification.get('transistors_density')
        )
        self.cores = GPUSpecification(name='cores', raw_specification=specification.get('cores'))
        self.sm = GPUSpecification(name='sm', raw_specification=specification.get('sm'))
        self.tpcs = GPUSpecification(name='tpcs', raw_specification=specification.get('tpcs'))
        self.tmus = GPUSpecification(name='tmus', raw_specification=specification.get('tmus'))
        self.rops = GPUSpecification(name='rops', raw_specification=specification.get('rops'))
        self.base_clock = GPUSpecification(name='base_clock', raw_specification=specification.get('base_clock'))
        self.boost_clock = GPUSpecification(name='boost_clock', raw_specification=specification.get('boost_clock'))
        self.memory_clock = GPUSpecification(name='memory_clock', raw_specification=specification.get('memory_clock'))
        self.effective_memory_clock = GPUSpecification(
            name='effective_memory_clock', raw_specification=specification.get('effective_memory_clock')
        )
        self.memory_size = GPUSpecification(name='memory_size', raw_specification=specification.get('memory_size'))
        self.memory_type = GPUSpecification(name='memory_type', raw_specification=specification.get('memory_type'))
        self.memory_bus_width = GPUSpecification(
            name='memory_bus_width', raw_specification=specification.get('memory_bus_width')
        )
        self.memory_bandwidth = GPUSpecification(
            name='memory_bandwidth', raw_specification=specification.get('memory_bandwidth')
        )
        self.interface = GPUSpecification(name='interface', raw_specification=specification.get('interface'))
        self.width = GPUSpecification(name='width', raw_specification=specification.get('width'))
        self.length = GPUSpecification(name='length', raw_specification=specification.get('length'))
        self.power_connectors = GPUSpecification(
            name='power_connectors', raw_specification=specification.get('power_connectors')
        )
        self.tdp_tbp = GPUSpecification(name='tdp_tbp', raw_specification=specification.get('tdp_tbp'))
        self.recommended_psu = GPUSpecification(
            name='recommended_psu', raw_specification=specification.get('recommended_psu')
        )
        self.dvi_i_duallink = GPUSpecification(
            name='dvi_i_duallink', raw_specification=specification.get('dvi_i_duallink')
        )
        self.s_video = GPUSpecification(name='s_video', raw_specification=specification.get('s_video'))
        self.directx = GPUSpecification(name='directx', raw_specification=specification.get('directx'))
        self.vulkan = GPUSpecification(name='vulkan', raw_specification=specification.get('vulkan'))
        self.opengl = GPUSpecification(name='opengl', raw_specification=specification.get('opengl'))
        self.opencl = GPUSpecification(name='opencl', raw_specification=specification.get('opencl'))
        self.pixel_fillrate = GPUSpecification(
            name='pixel_fillrate', raw_specification=specification.get('pixel_fillrate')
        )
        self.texture_fillrate = GPUSpecification(
            name='texture_fillrate', raw_specification=specification.get('texture_fillrate')
        )
        self.peak_fp32 = GPUSpecification(name='peak_fp32', raw_specification=specification.get('peak_fp32'))
        self.fp32_perf_per_watt = GPUSpecification(
            name='fp32_perf_per_watt', raw_specification=specification.get('fp32_perf_per_watt')
        )
        self.fp32_perf_per_mm2 = GPUSpecification(
            name='fp32_perf_per_mm2', raw_specification=specification.get('fp32_perf_per_mm2')
        )


class GPUSpecification:
    specifications_with_units = [
        'fabrication_process',
        'die_size',
        'transistors_count',
        'transistors_density',
        'base_clock',
        'boost_clock',
        'memory_clock',
        'effective_memory_clock',
        'memory_size',
        'memory_type',
        'memory_bandwidth',
        'width',
        'length',
        'height',
        'tdp_tbp',
        'recommended_psu',
        'pixel_fillrate',
        'texture_fillrate',
        'peak_fp32',
        'fp32_perf_per_watt',
        'fp32_perf_per_mm2',
    ]

    def __init__(self, name, raw_specification):
        self.name = self._standarize_specification_name(name)
        self.value, self.unit = self._read_raw_specification(name, raw_specification)

    def _read_raw_specification(self, name: str, raw_specification: str):
        name = self._standarize_specification_name(name)
        if name in self.specifications_with_units:
            raw_specification = raw_specification.split(' ')
            value = raw_specification[0]
            unit = raw_specification[1]
            return value, unit
        else:
            return raw_specification, None

    def _standarize_specification_name(self, name):
        return name.lower().replace(' ', '_').replace('.', '')
