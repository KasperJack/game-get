import pyhocon
import json
from typing import Any

from model import OSBlock, RootRelease,validate
from pydantic import ValidationError

from pathlib import Path
from errors import StructureError,ParseError,TypeMismatchError,NotFoundError
from pyparsing import ParseSyntaxException









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
    



def validate_root(data: dict):
    if "namespace" not in data:
        raise ValueError("Missing 'namespace' key")

    if not isinstance(data["namespace"], dict):
        raise TypeError("'namespace' must be a dictionary")
    


def validate_namespace_entries(namespace: dict):
    for name, value in namespace.items():
        if not isinstance(value, dict):
            raise TypeError(f"{name} must be a dictionary")
        





def validate_block(name: str, block: dict):
    ALLOWED_KINDS = {"Option", "Selection"}
    # kind
    if "kind" not in block:
        raise ValueError(f"{name}: missing 'kind'")
    if block["kind"] not in ALLOWED_KINDS:
        raise ValueError(f"{name}: invalid kind '{block['kind']}'")

    # description
    if "description" not in block:
        raise ValueError(f"{name}: missing 'description'")
    if not isinstance(block["description"], str):
        raise TypeError(f"{name}: description must be a string")

    # reserved_flags
    if "reserved_flags" not in block:
        raise ValueError(f"{name}: missing 'reserved_flags'")

    flags = block["reserved_flags"]

    if not isinstance(flags, list):
        raise TypeError(f"{name}: reserved_flags must be a list")

    if len(flags) < 2:
        raise ValueError(f"{name}: reserved_flags must have at least 2 items")

    if not all(isinstance(f, str) for f in flags):
        raise TypeError(f"{name}: all reserved_flags must be strings")

    if len(flags) != len(set(flags)):
        raise ValueError(f"{name}: reserved_flags must be unique")
    


def validate_global_flags(namespace: dict):
    seen = {}

    for name, block in namespace.items():
        for flag in block["reserved_flags"]:
            if flag in seen:
                raise ValueError(
                    f"Flag '{flag}' used in both '{seen[flag]}' and '{name}'"
                )
            seen[flag] = name



def validate_namespace_file(data: dict):
    validate_root(data)

    namespace = data["namespace"]

    validate_namespace_entries(namespace)

    for name, block in namespace.items():
        validate_block(name, block)

    validate_global_flags(namespace)



def load_namespace(path: Path):
    d = load_hocon_file(path)
    validate_namespace_file(d)


package_path = Path("C:\\Users\\Aya\\Desktop\\pact\\tools\\compiler_cli\\buckets\\defult\\cy\\cy2\\HOCON\\namespace.conf")    
load_namespace(package_path)