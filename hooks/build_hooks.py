import importlib.util
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

HERE = Path(__file__).parent


class ProcessDataHook(BuildHookInterface):
    def initialize(self, version, build_data):
        process_md = _load("process_data_md", "process_data_md.py").initialize
        embed_version = _load("embed_version", "embed_version.py").initialize

        process_md(Path(self.root), version, build_data)
        embed_version(Path(self.root), version, build_data)

        build_data["force_include"]["src/lcedfd/data"] = "lcedfd/data/"
        build_data["force_include"]["src/lcedfd/_version.py"] = "lcedfd/_version.py"


def _load(name, file):
    spec = importlib.util.spec_from_file_location(name, HERE / file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
