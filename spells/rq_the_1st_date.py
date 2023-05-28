import datetime
from redis import Redis
from rq import Queue


def long_loop():
    result = 0
    for i in range(10_000_000):
        result += i

    return result


def short_loop():
    result = 0
    for i in range(100):
        result += i

    return result


q = Queue(connection=Redis())
job = q.enqueue(long_loop)
print(job.result)

job2 = q.enqueue_in(datetime.timedelta(seconds=10), short_loop)
print(job2.result)