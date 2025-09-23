"""Compatibility module exposing the standardised Doc-Entities app."""

from importlib import util
from pathlib import Path
import sys
import types

SERVICE_DIR = Path(__file__).resolve().parent

if __package__:
    from .app_v1 import app  # type: ignore  # noqa: F401
else:  # pragma: no cover - executed when imported as top-level module
    module_path = SERVICE_DIR / "app_v1.py"
    package_name = "doc_entities"
    if "it_logging" not in sys.modules:
        logging_module = types.ModuleType("it_logging")

        def _setup_logging(app, service_name):  # pragma: no cover - shim for tests
            return app

        logging_module.setup_logging = _setup_logging  # type: ignore[attr-defined]
        sys.modules["it_logging"] = logging_module

    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SERVICE_DIR)]
        sys.modules[package_name] = package
        models_spec = util.spec_from_file_location(
            f"{package_name}.models", SERVICE_DIR / "models.py"
        )
        if models_spec and models_spec.loader:
            models_module = util.module_from_spec(models_spec)
            models_module.__package__ = package_name
            models_module.__path__ = [str(SERVICE_DIR / "models")]
            sys.modules[f"{package_name}.models"] = models_module
            models_spec.loader.exec_module(models_module)
        api_models_spec = util.spec_from_file_location(
            f"{package_name}.models.api_models", SERVICE_DIR / "models" / "api_models.py"
        )
        if api_models_spec and api_models_spec.loader:
            api_models_module = util.module_from_spec(api_models_spec)
            api_models_module.__package__ = f"{package_name}.models"
            sys.modules[f"{package_name}.models.api_models"] = api_models_module
            api_models_spec.loader.exec_module(api_models_module)

    module_name = f"{package_name}.app_v1"
    spec = util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError("Unable to load app_v1 module")
    module = util.module_from_spec(spec)
    module.__package__ = package_name
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    app = module.app  # type: ignore[attr-defined]

__all__ = ["app"]
