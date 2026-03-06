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