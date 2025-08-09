import pkgutil
import importlib
from aiogram import Router

def get_routers() -> list[Router]:
    routers = []
    package = __name__

    for _, module_name, _ in pkgutil.iter_modules(__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        if hasattr(module, "router"):
            routers.append(module.router)

    return routers
