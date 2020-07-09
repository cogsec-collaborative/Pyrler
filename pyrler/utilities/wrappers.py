from pyrler.utilities.logger import logger


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
                if r.json().get("last"):
                    break
                startkey = r.json()["next"]
            return data
        else:
            return func(*args, **kwargs)

    return func_wrapper
