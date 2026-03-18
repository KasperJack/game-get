class RegistryError(Exception):
    pass


class ManifestError(RegistryError):
    pass





#missing manifest errors

class IndexManifestNotFoundError(ManifestError):
    def __init__(self, package: str):
        super().__init__(f"Index manifest not found for package '{package}'")
        self.package = package


class VersionManifestNotFoundError(ManifestError):
    def __init__(self, package: str):
        super().__init__(f"Version manifest not found for package '{package}'")
        self.package = package

#invalid JSON errors

class InvalidIndexManifestError(ManifestError):
    def __init__(self, package: str):
        super().__init__(f"Invalid index manifest for package '{package}'")
        self.package = package


class InvalidVersionManifestError(ManifestError):
    def __init__(self, package: str):
        super().__init__(f"Invalid version manifest for package '{package}'")
        self.package = package

#missing key errors

class MissingKeyError(ManifestError):
    def __init__(self, key: str, package: str):
        super().__init__(f"Missing key '{key}' in package '{package}' manifest")
        self.key = key
        self.package = package

class MissingIndexKeyError(MissingKeyError):
    pass


class MissingVersionKeyError(MissingKeyError):
    pass



















class PackageManagerError(Exception): 
    pass


class LoaderError(PackageManagerError): 
    pass
class InstallationError(PackageManagerError): 
    pass


class FileSystemError(PackageManagerError): 
    pass
class ValidationError(PackageManagerError):
    pass


class MissingManifestError(LoaderError, FileSystemError):
    exit_code = 4
    def __init__(self, package_name: str, path: str):
        super().__init__(f"Version manifest not found for package '{package_name}'")
        self.package = package_name
        self.path = path
    


class MissingKeyError(LoaderError, ValidationError):
    exit_code = 5
    def __init__(self, key: str, package_name: str, path: str):
        super().__init__(f"Missing key '{key}' in package '{package_name}' manifest")
        self.key = key
        self.package_name = package_name
        self.path = path