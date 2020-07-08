import re
import inspect
from pyrler.utilities.logger import logger


def _rate_limit(response):
    retry_after = response.headers.get("Retry-After")
    pass


def _yolo_timestamp(response):
    pass


def paginate(func):
    def func_wrapper(*args, **kwargs):
        if kwargs.get("follow"):
            data = []
            if kwargs.get("startkey"):
                startkey = kwargs.get("startkey")
            else:
                startkey = None
            while True:
                r = func(startkey=startkey, *args, **kwargs)
                data.append(r)
                if r.json()["last"] == True:
                    break
                startkey = r.json()["next"]
            return data
        else:
            return func(*args, **kwargs)

    return func_wrapper
