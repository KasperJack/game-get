from core import Loader
from pathlib import Path
from core import LoaderError

TEST_BUCKET_PATH = Path.cwd() / "bucket -game-based"

l = Loader(TEST_BUCKET_PATH)




pkg = l.load(package_name="test",source="d")

