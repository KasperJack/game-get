
from datetime import date
from typing import Literal, Any
from pydantic import BaseModel,ConfigDict


class BoolNamespace(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["bool"]
    description: str
    reserved_flags: list[str]


class EnumNamespace(BaseModel):
    model_config = ConfigDict(extra="forbid")
    
    type: Literal["enum"]
    description: str


# union type
Namespace = BoolNamespace | EnumNamespace


class NamespaceRegistry(BaseModel):
    namespaces: dict[str, Namespace]

    def get(self, name: str) -> Namespace | None:
        return self.namespaces.get(name)




class BoolInterface(BaseModel):
    namespace: str              # only set on public interfaces
    local_var: str
    flags: list[str]
    default: str | bool | None
    description: str = ""       # inherited from namespace on public

    @property
    def full_path(self) -> str:
        return f"interface.{self.namespace}.{self.local_var}"


# ─── Interface Containers ─────────────────────────────────────────────────────

class PublicInterfaces(BaseModel):
    bool: dict[str, BoolInterface] = {}
    # string: dict[str, StringInterface] = {}   <- coming later
    # enum:   dict[str, EnumInterface]   = {}   <- coming later


class PrivateInterfaces(BaseModel):
    bool: dict[str, BoolInterface] = {}
    # string: dict[str, StringInterface] = {}   <- coming later
    # enum:   dict[str, EnumInterface]   = {}   <- coming later


# ─── Entity ───────────────────────────────────────────────────────────────────

class Entity(BaseModel):
    id: str
    source: str
    released: date
    version: str
    public_interfaces:  PublicInterfaces  = PublicInterfaces()
    private_interfaces: PrivateInterfaces = PrivateInterfaces()


# ─── Entity Loader ────────────────────────────────────────────────────────────