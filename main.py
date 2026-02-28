#from core.loader import load_package

from core import load_package, InvalidManifestError, PackageNotFoundError
import sys

def show_package_info(package_name: str):
    pass


def install_package(package_name: str):

    try:
        pkg = load_package(package_name)
    except PackageNotFoundError as e:
        print(e)
        # suggest another packages with close name 
        sys.exit(1)
    except InvalidManifestError as e:
        print(e)
        sys.exit(2)

    print(pkg.igdb_id)

install_package("ion-fury")