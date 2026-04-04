from core import TargetLoader
from pathlib import Path
from core import LoaderError

TEST_BUCKET_PATH = Path.cwd() / "bucket -game-based" 

l = TargetLoader(bucket_path=TEST_BUCKET_PATH, package_name="test")




pkg = l.load()

