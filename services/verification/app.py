"""Compatibility module exposing the v1 verification app."""

from importlib import util
from pathlib import Path
import sys
import types

SERVICE_DIR = Path(__file__).resolve().parent

if __package__:
    from .app_v1 import app  # type: ignore  # noqa: F401
else:  # pragma: no cover - executed when imported as top-level module
    module_path = SERVICE_DIR / "app_v1.py"
    package_name = "verification_service"

    if package_name not in sys.modules:
        package = types.ModuleType(package_name)
        package.__path__ = [str(SERVICE_DIR)]
        sys.modules[package_name] = package

        models_init = SERVICE_DIR / "models" / "__init__.py"
        models_module_name = f"{package_name}.models"
        models_spec = util.spec_from_file_location(models_module_name, models_init)
        if models_spec and models_spec.loader:
            models_module = util.module_from_spec(models_spec)
            models_module.__package__ = models_module_name
            models_module.__path__ = [str(SERVICE_DIR / "models")]
            sys.modules[models_module_name] = models_module
            models_spec.loader.exec_module(models_module)

        api_models_path = SERVICE_DIR / "models" / "api_models.py"
        api_models_name = f"{package_name}.models.api_models"
        api_models_spec = util.spec_from_file_location(api_models_name, api_models_path)
        if api_models_spec and api_models_spec.loader:
            api_models_module = util.module_from_spec(api_models_spec)
            api_models_module.__package__ = models_module_name
            sys.modules[api_models_name] = api_models_module
            api_models_spec.loader.exec_module(api_models_module)

    module_name = f"{package_name}.app_v1"
    spec = util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:  # pragma: no cover - defensive
        raise ImportError("Unable to load verification app_v1 module")
    module = util.module_from_spec(spec)
    module.__package__ = package_name
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    app = module.app  # type: ignore[attr-defined]

__all__ = ["app"]
