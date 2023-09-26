import importlib
import os.path
from types import ModuleType
from typing import List


def load_modules_from_project_directory(path: str,
                                        module_fullname=None,
                                        ignore_files: List[str] =
                                        None, recursive=False) -> List[ModuleType]:
    if ignore_files is None:
        ignore_files = []

    ignore_files.append("__init__.py")
    full_path = os.path.realpath(path)
    assert os.path.isdir(full_path), f"{full_path} is not a directory"

    python_files = [f for f in os.listdir(full_path)
                    if os.path.isfile(os.path.join(full_path, f)) and f.endswith(".py")]

    modules = []
    for python_file in python_files:
        if python_file not in ignore_files:
            python_module = python_file.replace('.py', '')

            package_def = [] if module_fullname is None else [module_fullname]
            package_def.append(python_module)
            python_module_full_name = ".".join(package_def)

            lib = importlib.import_module(python_module_full_name)
            modules.append(lib)

    if recursive:
        packages = [f for f in os.listdir(full_path) if os.path.isdir(os.path.join(full_path, f))]
        for package in packages:
            modules += load_modules_from_project_directory(os.path.join(path, package),
                                                           f"{module_fullname}.{package}",
                                                           ignore_files=ignore_files,
                                                           recursive=recursive)

    return modules
    