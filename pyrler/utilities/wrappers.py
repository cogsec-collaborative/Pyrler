from pyrler.utilities.logger import logger


def _yolo_timestamp(response):
    pass


def paginate(func):
    def func_wrapper(*args, **kwargs):
        if kwargs.get("follow"):
            data = []
            # Start at user defined index otherwise get the most recent page.
            if kwargs.get("startkey"):
                startkey = kwargs.get("startkey")
            else:
                startkey = None

            # Fetch pages until we've got them or something breaks.
            while True:
                r = func(startkey=startkey, *args, **kwargs)
                data.append(r)

                # Break on the last page.
                if r.json().get("last"):
                    logger.debug("Found last page.")
                    break

                # Break if the endpoint doesn't return a next page index.
                if not r.json().get("next"):
                    logger.debug("Next page not returned.")
                    break

                # Break if the next value of the current request is the same as startkey from the last request.
                # urllib3.util.retry uses Retry with incremental back off and transparently handles HTTP errors
                # and rate-limit.  If the next param is the same as the previous value it means we performed two
                # iterations of the incremental backoff limit and something is broken.
                # This prevents the while loop from looping forever.
                if startkey == r.json().get("next"):
                    logger.debug("Next page could not be returned. Check requests debug log.")
                    break

                startkey = r.json().get("next")
            return data
        else:
            return func(*args, **kwargs)

    return func_wrapper
