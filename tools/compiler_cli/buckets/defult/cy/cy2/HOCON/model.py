from pydantic import BaseModel, ConfigDict
from typing import List, Literal

class OptionBlock(BaseModel):
    model_config = ConfigDict(extra="forbid")  

    kind: Literal["Option", "Selection"]
    description: str
    reserved_flags: List[str]