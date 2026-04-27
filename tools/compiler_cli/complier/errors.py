from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path






class PackageNotFoundError(Exception):
    exit_code = 4
    def __init__(self, path: Path):
        package_name = _infer_package_name(path)
        super().__init__(f"pacakge'{package_name}' not found")
        self.package = package_name
        self.path = path



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















class BaseError(Exception):
    def __init__(self, message: str, *, cause: Exception | None = None, **context):
        self.message = message
        self.context = context
        self.cause = cause
        super().__init__(message)

    @property
    def error_type(self):
        return self.__class__.__name__

    def __str__(self):
        lines = [f"Error: {self.error_type}", " |"]

        for k, v in self.context.items():
            lines.append(f" | {k}: {v}")

        if self.cause:
            lines.append(f" | cause: {repr(self.cause)}")

        lines.append(" |")
        lines.append(f" | {self.message}")

        return "\n".join(lines)



class NamespaceFileNotFound(BaseError):
    def __init__(self, path:str):
        super().__init__(
            message = "Namespace file not found",
            path=path,
  
        )


class ConfigParseError(BaseError):
    pass

class ConfigConversionError(BaseError):
    pass