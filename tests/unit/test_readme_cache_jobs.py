import gcip
from tests import conftest


def test():
    pipeline = gcip.Pipeline()
    cache = gcip.Cache(["dir1", "dir2", "dir3/subdir"])
    cachejob1 = gcip.Job(name="cachejob1", namespace="single-stage", script="date")
    cachejob2 = gcip.Job(name="cachejob2", namespace="single-stage", script="date")
    cachejob1.set_cache(cache)
    cachejob2.set_cache(cache)
    pipeline.add_children(cachejob1, cachejob2)

    conftest.check(pipeline.render())
