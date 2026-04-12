from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path



def _infer_release(path: Path) -> str:
    return path.parent.name

def _infer_package_name(path: Path) -> str:
    parts = path.parts
    for i, part in enumerate(parts):
        if len(part) == 2 and i + 1 < len(parts):
            return parts[i + 1]
    return "could not infer package name from path"



class PackageNotFoundError(Exception):
    exit_code = 4
    def __init__(self, path: Path):
        package_name = _infer_package_name(path)
        super().__init__(f"pacakge'{package_name}' not found")
        self.package = package_name
        self.path = path


class NamespaceFileNotFound(Exception):
    def __init__(self, path: Path):
        package_name = _infer_package_name(path)
        path_str     = f"{path.parent}\\[{path.name}] <-- missing"

        super().__init__(
            f"Namespace file not found for package '{package_name}'\n"
            f"{path_str}"
        )
        self.package = package_name
        self.path    = path


class EntityNotFound(Exception):
    def __init__(self, path: Path):
        package_name = _infer_package_name(path)
        release      = _infer_release(path)
        path_str     = f"{path.parent}\\[{path.name}] <-- missing"

        super().__init__(
            f"Entity file not found for release '{release}' in package '{package_name}'\n"
            f"{path_str}"
        )
        self.package = package_name
        self.release = release
        self.path    = path