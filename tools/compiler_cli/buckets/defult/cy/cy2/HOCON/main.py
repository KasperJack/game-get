import pyhocon
import json
from typing import Any

from model import OSBlock, RootRelease,validate
from pydantic import ValidationError

from pathlib import Path
from errors import StructureError,ParseError,TypeMismatchError,NotFoundError
from pyparsing import ParseSyntaxException



def load_namespace(package_path: Path) -> dict[str,OSBlock] :



    file_path = package_path / "namespace.conf"


    if not file_path.exists():
            raise NotFoundError(
                "The namespace file could not be located",
                package="test",
                file=file_path
                )
    




    try:
        config = load_hocon_file(file_path)

    except ParseSyntaxException as e:
        raise ParseError(
            "Failed to parse Namespace file",
            original=str(e),
            package="libtree",
            release="official_1.5",
            file=file_path
        ) from e


    #config = load_hocon_file(file_path)




   
    namespace = config.get("namespace")

    if namespace == None:
            raise StructureError(
                "Root definition `namespace` is missing",
                package="test",
                release="official_test",
                file=file_path
                )
  
    
   
    if not isinstance(namespace,dict):
            raise TypeMismatchError(
                f"Root definition `namespace` must be a mapping, got {type(namespace).__name__}",
                package="test",
                release="official_test",
                file=file_path
                )

    ########

    parsed = {}
    for name, value in namespace.items():

        if not isinstance(value, dict):
                raise TypeMismatchError(
                    f"Expected a mapping for field `{name}`, found {type(value).__name__}",
                    package="test",
                    release="official_test",
                    file=file_path
                    )

        #err = validate(OptionBlock,value)      
        #print(repr(err))
        
        parsed[name] = OSBlock.model_validate(value)
        

    ## check for cross key uniqeness 
    ensure_global_flag_uniqueness(parsed)
    return parsed



def ensure_global_flag_uniqueness(objects: dict[str, OSBlock]):
    seen = set()

    for name, osb in objects.items():
        for flag in osb.reserved_flags:
            if flag in seen:
                raise ValueError(f"Flag '{flag}' is duplicated across objects (found in {name})")
            seen.add(flag)








def check_entity(namesapce: dict[str,OSBlock] | None , config: dict):

    
    using = config.get("using")
    print(using)



    match using:
        case str():
            print("str")
        case list():
            print("list")
        
        case None:
            print("none")

        case _:
            print('wtf')


    release = config.get("release")
    if release == None:
        raise Exception("Release defention not found !")


    if not isinstance(release,dict):
        raise Exception("Release defention should be a dict !")


    allowed_blocks = ["meta","tags","public","private"]

    for name, value in release.items():

        if name not in allowed_blocks:
            raise Exception(f"unexpacted key {name}")

        if not isinstance(value,dict):
            raise Exception(f"{name} defention should be a dict !")


    tags = release.get("tags")
    public = release.get("public")
    private = release.get("private")














def validate_declaration_release(path: Path) -> dict[str, Any]:
    """check file declares the expected root keys"""
    

        
    config = load_hocon_file(path)


    try:
        RootRelease.model_validate(config)
    except ValidationError as e:
        errors = e.errors()
        msg = f"invalid release contract in {path}:\n"
        for err in errors:
            field = " -> ".join(str(loc) for loc in err["loc"])
            msg  += f"  {field}: {err['msg']}\n"
        raise ValueError(msg)

    
    return config






def load_hocon_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"{path} does not exist")

    try:
        config = pyhocon.ConfigFactory.parse_file(path)
    except Exception as e:
        raise ValueError(f"Failed to parse HOCON: {e}")

    try:
        return json.loads(json.dumps(config))
    except Exception as e:
        raise ValueError(f"Failed to convert config to dict: {e}")



def load_releases(package_path: Path) -> dict[Path, dict]:
    releases_dir = package_path / "releases"
    
    if not releases_dir.exists():
        raise FileNotFoundError(f"missing releases directory: {releases_dir}")

    results = {}

    for version_dir in releases_dir.iterdir():
        
        if not version_dir.is_dir():
            continue
        
        release_file = version_dir / "release.conf"
        
        # empty folder
        if not release_file.exists():
            raise NotFoundError(
                "The namespace file could not be located",
                package="test",
                file=release_file,
                release="official_test",
                )
        
        # validates declaration and loads
        config = validate_declaration_release(release_file)
        results[version_dir] = config

        

    return results















if __name__ == "__main__":

    package_path = Path("C:\\Users\\Aya\\Desktop\\pact\\tools\\compiler_cli\\buckets\\defult\\cy\\cy2\\HOCON")

    nsp = load_namespace(package_path)


    #load_releases(package_path)
