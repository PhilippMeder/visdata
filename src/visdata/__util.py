import sys


def get_module(name: str) -> object:
    # Follow 'sys' documentation and avoid possible errors
    modules = sys.modules.copy()
    for module_name, module in modules.items():
        if module_name == name:
            return module
    else:
        raise ModuleNotFoundError(f"Can't find module '{name}'!")


def get_numpy() -> object:
    return get_module("numpy")
