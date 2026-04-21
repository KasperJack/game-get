import pyhocon
import json
from typing import Any

from model import OptionBlock
from pydantic import ValidationError


def check_namespace(config: dict[str,Any]) -> dict[str,OptionBlock]:

    parsed = {}
    namespace = config.get("namespace")

    if namespace == None:
        raise Exception("Namespace defention not found !")
    
   


    for name, value in namespace.items():
        if not isinstance(value, dict):
            raise TypeError(f"{name} is not a dict")

        try:
            parsed[name] = OptionBlock(**value)

        except ValidationError as e:
            errors = []
            for err in e.errors():
                field = ".".join(str(x) for x in err["loc"])
                msg = err["msg"]
                errors.append(f"{name}.{field}: {msg}")

            raise ValueError("\n".join(errors))

    return parsed




if __name__ == "__main__":
    config = pyhocon.ConfigFactory.parse_file("namespace.conf")
    config = json.loads(json.dumps(config))
    p = check_namespace(config)

    print(p["download"].reserved_flags)

