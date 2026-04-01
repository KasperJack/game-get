import tomllib
from pathlib import Path
from .models import PackageManifest
from .resolver import resolver
from .exceptions import MissingManifestError,InvalidManifestError,MissingKeyError,PackageNotFoundError, PackageEmptyError
from typing import Any, Callable, cast
from enum import Enum





class ManifestType(Enum):
    PACKAGE = "game"
    REGISTRY = "registry"
    RELEASE = "release"
    DOWNLOAD = "download"

    @property
    def filename(self) -> str:
        return f"{self.value}.toml"









class PackageComponent(Enum):
    SOURCES = "source"
    VERSIONS = "version"
    METHODS = "method"




class BaseLoader:

    """
    All filesystem work lives here.
    Scans directories, reads TOML files, throws file-related errors.
    """

    def __init__(self, bucket_path: str | Path, package_name: str):
        self.bucket_path = Path(bucket_path)
        self.package_name = package_name
        self.package_path = self._find_package(package_name)




    def _find_package(self, package_name: str) -> Path:

        prefix = package_name[:2]
        package_path = self.bucket_path / prefix / package_name
        
        if package_path.is_dir():
            return package_path
        else:
            raise PackageNotFoundError




    def load_package_manifest(self) -> dict[str, Any]:

        package_file_path = self.package_path / ManifestType.PACKAGE.filename
        return self._load_manifest(package_file_path, ManifestType.PACKAGE)
    




    def load_registry_manifest(self, source: str) -> dict[str, Any]:

        registry_file_path = self.package_path / source / ManifestType.REGISTRY.filename
        return self._load_manifest(registry_file_path, ManifestType.REGISTRY)




    def load_release_manifest(self, source: str, version: str) -> dict[str, Any]:

        release_file_path = self.package_path / source / version / ManifestType.RELEASE.filename
        return self._load_manifest(release_file_path, ManifestType.RELEASE)

    


    def load_download_manifest(self, source: str, version: str, method: str) -> dict[str, Any]:

        download_file_path = self.package_path / source / version / method / ManifestType.DOWNLOAD.filename
        return self._load_manifest(download_file_path, ManifestType.DOWNLOAD)





    def get_available_sources(self) -> list[str]:

        ignore_dir = ["steam_builds"]
        available_sources = self._scan_dir(self.package_path, ignore_dir)

        if len(available_sources) == 0:
            raise PackageEmptyError(self.package_path, PackageComponent.SOURCES)
        
        return available_sources






    def get_available_versions(self, source: str) -> list[str]:
        versions_path = self.package_path / source

        available_versions = self._scan_dir(versions_path)

        if len(available_versions) == 0:
            raise PackageEmptyError(versions_path, PackageComponent.VERSIONS)
        
        return available_versions




    def get_available_methods(self, source: str, version: str) -> list[str]:
        meathods_path = self.package_path / source / version

        available_methods = self._scan_dir(meathods_path)

        if len(available_methods) == 0:
            raise PackageEmptyError(meathods_path, PackageComponent.METHODS)
        
        return available_methods






    def _load_manifest(
        self,
        file_path: Path,
        manifest_type: ManifestType,
        #validator: Callable[[dict[str, Any], Path], None],
    ) -> dict[str, Any]:
        

        if not file_path.is_file():
            raise MissingManifestError(file_path, manifest_type)

        try:
            with open(file_path, "rb") as f:
                data = tomllib.load(f)
        except tomllib.TOMLDecodeError:
            raise InvalidManifestError(file_path, manifest_type)

        #validator(data, manifest_type)
        self._validate_keys(data,manifest_type)

        return data



    def _validate_keys(self, data: dict[str, Any], manifest_type: ManifestType):
        match manifest_type:
            case ManifestType.PACKAGE:
                raise NotImplementedError("package validator")
            case ManifestType.REGISTRY:
                ...
            case ManifestType.RELEASE:
                ...
            case ManifestType.DOWNLOAD:
                ...
            case _:
                raise RuntimeError(f"unhandled manifest type: {manifest_type}")




    def validate_keys_package(self,data: dict[str, Any], package_manifest_file_path: Path):
        required_keys = ["name", "default_version","release_year"]
        for key in required_keys:
            if key not in data:
                raise MissingKeyError(key,package_manifest_file_path, ManifestType.PACKAGE)
        
        ids = data.get("ids", {})
        if "igdb" not in ids:
            raise MissingKeyError("igdb",package_manifest_file_path, ManifestType.PACKAGE)








    def _scan_dir(self, target_path: Path, ignore: list[str] | None = None) -> list[str]:

        # If ignore is None, we treat it as an empty list to keep the logic clean
        to_ignore = ignore or []
        
        return [
            d.name for d in target_path.iterdir() 
            if d.is_dir() and d.name not in to_ignore
        ]
    




class TargetLoader(BaseLoader):

    def __init__(
        self,
        bucket_path: str | Path,
        package_name: str,
        source: str | None = None,
        version: str | None = None,
        method: str | None = None,
    ):
        super().__init__(bucket_path,package_name)

        self.source = source
        self.version = version
        self.method = method

    def load(self):

        

        package__manifest = self.load_package_manifest() ##raises an error "package not found"


        r = resolver(self, package__manifest, self.source, self.version, self.method)

   
        print(r.target_source,r.target_version,r.target_method)
        #return
        
        ## TODO: remove all this part later *
        ## build the data class that holds the resolved pacakge 
        ## figure out how to get metadata without building a full package instance 
        ##  add type checking for mainfest data 
