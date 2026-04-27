from pydantic import BaseModel, ConfigDict,field_validator,ValidationError,model_validator, ValidationInfo,Field

from typing import get_origin, get_args, Literal, Any, Optional,List,Annotated
from dataclasses import dataclass





class OSBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")  

    kind: Literal["Option", "Selection"]
    description: str
    reserved_flags: Annotated[List[str], Field(min_length=1, max_length=10)]

    @field_validator("reserved_flags")
    @classmethod
    def check_unique(cls, v):
        if len(v) != len(set(v)):
            raise ValueError("reserved_flags must contain unique items")
        return v

























if __name__ == "__main__":
    raw_data = {
        "kind": "Ogption",
        "description": "f",
        "reserved_flags":["5","4"],

}
    #print(OptionBlock.model_fields)

    err = validate(OptionBlock,raw_data)

    print(repr(err))






























VALID_USING = {"namespace package", "namespace global"}


class RootRelease(BaseModel):
    model_config = ConfigDict(extra="forbid")

    release:       dict   ## can be missing or have a worng tpye 
    using:         Optional[str] = None # can have a wrong type can be using non exisatnt name space 
    tool_metadata: Optional[Any] = None # don't care about this one 

    
    @field_validator("release")
    @classmethod
    def validate_release(cls, v):
        if not isinstance(v, dict):
            raise ValueError("release must be a block declaration: release {{ }}")
        return v



    @field_validator("using")
    @classmethod
    def validate_using(cls, v):
        if v is not None and v not in VALID_USING:
            raise ValueError(
                f"unknown directive '{v}'\n"
                f"  valid directives: {', '.join(VALID_USING)}"
            )
        return v

































































@dataclass
class MissingError:
    field: str

@dataclass
class ExtraError:
    field: str

@dataclass
class FieldError:
    field:    str
    got:      Any
    expected: str


class BlockErrors:
    def __init__(self):
        self.missing : list[MissingError] = []
        self.extra   : list[ExtraError]   = []
        self.fields  : list[FieldError]   = []

    def __bool__(self):
        return bool(self.missing or self.extra or self.fields)

    def __repr__(self):
        return (f"BlockErrors(missing={self.missing}, extra={self.extra}, "
                f"fields={self.fields})")




def validate(cls: type[BaseModel], data: dict) -> BlockErrors:
    err    = BlockErrors()

    fields = cls.model_fields



    dont_allow_extra = cls.model_config.get("extra") == "forbid"

    for name, field in fields.items():
        if name not in data:
            if field.is_required():
                err.missing.append(MissingError(field=name))

    for name in data:
        if name not in fields:
            if dont_allow_extra:
                err.extra.append(ExtraError(field=name))
            continue

        hint   = fields[name].annotation
        value  = data[name]
        origin = get_origin(hint)

        if hint is Any:
            pass

        elif origin is Literal:
            args = get_args(hint)
            if value not in args:
                err.fields.append(FieldError(
                    field    = name,
                    got      = value,
                    expected = " or ".join(repr(a) for a in args)
                ))

        elif origin is list:
            inner = get_args(hint)[0]
            meta  = fields[name].metadata

            if not isinstance(value, list):
                err.fields.append(FieldError(field=name, got=type(value).__name__, expected=f"list[{inner.__name__}]"))
            else:
                for m in meta:
                    if hasattr(m, 'min_length') and len(value) < m.min_length:
                        err.fields.append(FieldError(field=name, got=str(len(value)), expected=f"min {m.min_length} items"))
                    if hasattr(m, 'max_length') and len(value) > m.max_length:
                        err.fields.append(FieldError(field=name, got=str(len(value)), expected=f"max {m.max_length} items"))

                    
                    for idx, item in enumerate(value):
                        if not isinstance(item, inner):
                            err.fields.append(FieldError(field=f"{name}[{idx}]", got=type(item).__name__, expected=inner.__name__))
                            break
        else:
            if not isinstance(value, hint):
                err.fields.append(FieldError(
                    field    = name,
                    got      = type(value).__name__,
                    expected = hint.__name__
                ))

    return err