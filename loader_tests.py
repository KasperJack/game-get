from core import TargetLoader
from pathlib import Path
from core import LoaderError

TEST_BUCKET_PATH = Path.cwd() / "bucket -game-based" 

l = TargetLoader(TEST_BUCKET_PATH,"test",source="ass",version="12")




pkg = l.load()

