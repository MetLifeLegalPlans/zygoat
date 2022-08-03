import os

bind = "0.0.0.0:3000"
# While multiprocessing.cpu_count() would technically work, it gives us
# the number of CPUs attached to the system and not the number we can use.
# With core affinity being as fuzzy as it is for containerized workflows
# and vCPU units being vague, this should get us a more accurate number.
workers = max(1, len(os.sched_getaffinity(0))) * 2 + 1
try:
    from gevent import monkey
    from psycogreen.gevent import patch_psycopg

    worker_class = "gevent"

    def do_post_fork(server, worker):
        monkey.patch_all()
        patch_psycopg()

        worker.log.info("Running green threads")

    post_fork = do_post_fork
except ImportError:
    pass
