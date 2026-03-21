from core import Loader
from pathlib import Path
from core import LoaderError

TEST_BUCKET_PATH = Path.cwd() / "bucket -game-based"

l = Loader(TEST_BUCKET_PATH)



try:
    pkg = l.load("test",source="ass")

except LoaderError as e:
    print(e)

