#from core.loader import load_package
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.models import Package,Version


from core import load_package,PackageManager, IndexManifestNotFoundError,InvalidIndexManifestError,MissingIndexKeyError
import sys




def install_package(package_name: str):

    try:
        # try to check of defult version is defined porpely 
        # check missing keys errors 
        pkg = load_package(package_name)
    except IndexManifestNotFoundError as e:
        print(e)
        # suggest another packages with close name 
        sys.exit(1)
    except InvalidIndexManifestError as e:
        print(e)
        sys.exit(2)

    pm = PackageManager()
    
install_package("dead-cells")