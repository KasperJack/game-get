from __future__ import annotations
import tomllib
from pathlib import Path
from .errors import NamespaceFileNotFound,EntityNotFound

def load_namespace_file(path: Path) -> dict:
    if not path.exists():
        raise NamespaceFileNotFound(path)
    with path.open("rb") as f:
        return tomllib.load(f)


def load_entities(paths: list[Path]) -> dict[Path, dict]:
    results = {}
    for p in paths:
        p = Path(p)
        if not p.exists():
            raise EntityNotFound(p)
        with p.open("rb") as f:
            results[p] = tomllib.load(f)
    return results