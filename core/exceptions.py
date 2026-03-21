
""""
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





"""


class PackageManagerError(Exception): 
    pass

class LoaderError(PackageManagerError): 
    pass

"""
class InstallationError(PackageManagerError): 
    pass

class FileSystemError(PackageManagerError): 
    pass
class ValidationError(PackageManagerError):
    pass
"""

class ResolutionError(LoaderError):
    """Base for when we can't figure out which files to use"""
    exit_code = 7

#loader

class PackageNotFoundError(LoaderError):
    pass


class MissingManifestError(LoaderError):
    exit_code = 4
    def __init__(self, package_name: str, path: str, manifest_type: str = "package"):
        super().__init__(f" {manifest_type} manifest not found for package '{package_name}'")
        self.package = package_name
        self.path = path
        self.manifest_type = manifest_type
        # debug 
       
    
class InvalidManifestError(LoaderError):
    ## in the case of malformed toml
    def __init__(self, package_name: str, path: str, manifest_type: str = "package"):
        super().__init__(f"Invalid {manifest_type} manifest for package '{package_name}'")
        self.package_name = package_name
        self.path = path
        self.manifest_type = manifest_type

class MissingKeyError(LoaderError):
    exit_code = 5
    def __init__(self, key: str, package_name: str, path: str, manifest_type: str = "package"):
        super().__init__(f"Missing key '{key}' in package '{package_name}' manifest")
        self.key = key
        self.package_name = package_name
        self.path = path
        self.manifest_type = manifest_type

class PackageEmptyError(LoaderError):
    def __init__(self, package_name: str, path: str, item_type: str):
        super().__init__(f"Could not select {item_type} for '{package_name}'. No options found")
        self.package_name = package_name
        self.path = path
        self.item_type = item_type

class UserInputError(ResolutionError):
    """The user asked for something specific that doesn't exist"""
    def __init__(self, item_type: str, requested: str, available: list):
        # item_type: "source", "version", or "method"
        super().__init__(f"{item_type.capitalize()} '{requested}' not found. Available: {', '.join(available)}")
        self.requested = requested
        self.available = available

