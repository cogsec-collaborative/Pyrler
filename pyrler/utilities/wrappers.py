import re
import inspect
from pyrler.utilities.logger import logger

getargspec = inspect.getfullargspec
tag_pattern = re.compile("<\w[a-zA-Z0-9_]{0,31}>")


def _route_update(route, **kwargs):
    """
    Replaces <arg> in route.
    :param route: the route to be replaced
    :param kwargs:
    :return: updated route
    """
    replace = re.findall(tag_pattern, route)
    for tag in replace:
        key = str(tag.split("<")[1].split(">")[0])
        if key not in kwargs:
            raise KeyError("Route update failed. Missing arg: " + key)
        route = re.sub(tag, str(kwargs[key]), route)

    return route

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
