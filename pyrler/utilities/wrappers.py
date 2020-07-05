import re
import inspect
from functools import wraps

try:
    getargspec = inspect.getfullargspec
except Exception:
    getargspec = inspect.getargspec

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


def _default_args(func):
    """
    :param func:
    :return:
    """
    arg_dict = {}

    arg_data = getargspec(func)
    positional_args = arg_data[0]
    default_values = arg_data[3]
    if not default_values or not positional_args:
        return arg_dict

    start = len(positional_args) - len(default_values)

    for index in range(start, len(positional_args)):
        arg_dict[positional_args[index]] = default_values[index - start]

    return arg_dict


def _check_args(args, **kwargs):
    """
    Check if an argument exists and contains the correct data.
    Removes None type args.
    :param key: The argument to be checked, ex: params
    :param required: The required keys in the required argument's dictionary
    :param kwargs: The arguments passed in to be checked
    :return:
    """

    new_args = {}
    if not args:
        return new_args
    if not isinstance(args, list):
        raise TypeError("Expected required to be list")
    for parameter in args:
        if kwargs.get(parameter) is not None:
            new_args[parameter] = kwargs.get(parameter)
    return new_args


def template_request(method, route, request_params=None, json_body=None, request_headers=None):
    """
    Build request methods.
    :param method:
    :param route:
    :param request_params:
    :param json_body:
    :param request_headers:
    :return: function response
    """

    def decorate(func):
        @wraps(func)
        def wrap(self, *args, **kwargs):

            arg_data = getargspec(func)
            arg_vars = list(arg_data[0])

            if "self" in arg_vars:
                arg_vars.remove("self")

            for i in args:
                kwargs[arg_vars[args[i]]] = i

            defaults = _default_args(func)

            for k, v in defaults.items():
                if k not in kwargs:
                    kwargs[k] = v

            kwargs["route"] = _route_update(route=route, **kwargs)
            kwargs["method"] = method
            kwargs["params"] = _check_args(request_params, **kwargs)
            kwargs["json"] = _check_args(json_body, **kwargs)
            kwargs["headers"] = _check_args(request_headers, **kwargs)

            return func(self, **kwargs)

        return wrap

    return decorate
