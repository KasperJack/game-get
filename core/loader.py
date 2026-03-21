import tomllib
from pathlib import Path
from .models import Package, Version
from.resolver import resolver
from .exceptions import MissingManifestError,InvalidManifestError,MissingKeyError,PackageNotFoundError, PackageEmptyError
from dataclasses import dataclass
from typing import Any


class Loader:
    """
    All filesystem work lives here.
    Scans directories, reads TOML files, throws file-related errors.
    Uses Resolver for all decision logic.
    """
 
    def __init__(self, bucket_path: str | Path):
        self.bucket_path = Path(bucket_path)

    def load(
        self,
        package_name: str,
        source: str | None = None,
        version: str | None = None,
        method: str | None = None,
    ) -> Package:


        package_path = self._find_package(package_name) ##raise package not found error 

        package__index_data = self._get_package__index(package_path, package_name) ##raise 
        print(package__index_data)

        r = resolver(self, package_path,package_name,package__index_data,source,version,method)

        # call resover here ??
        #target: InstallTarget = resolve(package_path,index_data,source,version,method)
        print(r.target_source,r.target_version,r.target_method)
        #return
    
        ## later fix all this part 
        if version is None:
            version = index_data["default_version"]
        else:
            pass


        

        version_file_path = package_path / version / "manifest.json"


        if not version_file_path.is_file():
            raise VersionManifestNotFoundError(package_name)


        try:
            with open(version_file_path, "r", encoding="utf-8") as f:
                version_data = json.load(f)
        except json.JSONDecodeError:
            raise InvalidVersionManifestError(package_name)


        validate_keys_version(version_data,package_name)


        versions = {}
        for v in data["versions"]:
            versions[v["id"]] = Version(
                id=v["id"],
                version=v["version"],
                source=v["source"],
                size_mb=float(v["size_mb"]),
                notes=v["notes"],
                downloads=v["downloads"]
            )

        return Package(
            name=data["name"],
            release_year=data["release_year"],
            igdb_id=data["igdb_id"],
            default=data["default"],
            versions=versions
        )




    def _find_package(self, package_name: str) -> str:

        prefix = package_name[:2]
        package_path = self.bucket_path / prefix / package_name
        
        if package_path.is_dir():
            return package_path
        else:
            raise PackageNotFoundError


    def _get_package__index(self, package_path: str, package_name: str) -> dict[str, Any]:
        index_file_path = package_path / "index.toml"

        if not index_file_path.is_file():
            raise MissingManifestError(package_name,package_path,"index")


        try:
            with open(index_file_path, "rb") as f:  #bytes
                index_data = tomllib.load(f)
        except tomllib.TOMLDecodeError:
            raise InvalidManifestError(package_name,index_file_path,"index")

        #required keys
        self.validate_keys_index(index_data,index_file_path,package_name)
        
        return index_data



    ## used by resolver ?
    def get_available_sources(self, package_name: str ,package_path: str) -> list[str]:

        package_path = Path(package_path)
        available_sources = [
        p.name
        for p in package_path.iterdir()
        if p.is_dir() and p.name != "steam_builds"
        ]

        if len(available_sources) == 0:
            raise PackageEmptyError(package_name,package_path,"source")
        
        return available_sources


    def get_available_versions(self, package_name: str ,package_path: str, source: str) -> list[str]:
        versions_path = package_path / source

        available_versions = [
        d.name for d in versions_path.iterdir() if d.is_dir()
    ]

        if len(available_versions) == 0:
            raise PackageEmptyError(package_name,versions_path,"version")
        
        return available_versions


    def get_available_methods(self, package_name: str ,package_path: str, source: str, version: str) -> list[str]:
        meathods_path = package_path / source / version

        available_methods = [
        d.name for d in meathods_path.iterdir() if d.is_dir()
    ]

        if len(available_methods) == 0:
            raise PackageEmptyError(package_name,meathods_path,"method")
        
        return available_methods





    def validate_keys_index(self,data: dict, index_file_path: str, package_name: str):
        required_keys = ["name", "default_version"]
        for key in required_keys:
            if key not in data:
                raise MissingKeyError(key,package_name,index_file_path,"index")
        
        ids = data.get("ids", {})
        if "igdb" not in ids:
            raise MissingKeyError("igdb",package_name,index_file_path,"index")
            





    def validate_keys_version(data: dict, package_name: str):
        required_keys = ["name", "slug", "release_year","igdb_id","default","ass"]
        for key in required_keys:
            if key not in data:
                raise MissingVersionKeyError(key, package_name)
            




    def resolve(package_path,index_data, source, version, method) -> InstallTarget:
        # SOURCE
        sources = get_sources(package_path)

        if source:
            if source not in sources:
                raise SourceNotFound(source, sources)
        else:
            source = auto_select_source(index_data, sources)

        # VERSION
        versions = get_versions(package_path, source)

        if version:
            if version not in versions:
                raise VersionNotFound(version, versions)
        else:
            version = auto_select_version(index_data, source, versions)

        # METHOD
        methods = get_methods(package_path, source, version)

        if method:
            if method not in methods:
                raise MethodNotFound(method, methods)
        else:
            method = select_method(methods)





