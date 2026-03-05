from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Package, Download,Version




def download_package(pkg: Package):
    v: Version = pkg.versions[pkg.default]
    d: dict[str, Download] = v.downloads

    for download in d.values():
        print(download.type)
