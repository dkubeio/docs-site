from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

shared_path = Path(__file__).resolve().parent.parent / "conf_main.py"
spec = spec_from_file_location("conf_main", shared_path)
module = module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)

globals().update(module.build_conf(doc_version="v2.0.1", conf_file=__file__))