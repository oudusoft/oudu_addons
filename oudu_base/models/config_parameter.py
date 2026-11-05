TRUE_VALUES = frozenset(("1", "true", "t", "yes", "y", "on"))
FALSE_VALUES = frozenset(("0", "false", "f", "no", "n", "off"))

def get_string(params, key, default=False):
    getter = getattr(params, "get_str", None)
    if getter:
        return getter(key, default)
    return params.get_param(key, default)

def get_integer(params, key, default=0):
    getter = getattr(params, "get_int", None)
    if getter:
        return getter(key, default)
    value = params.get_param(key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default

def get_boolean(params, key, default=False):
    getter = getattr(params, "get_bool", None)
    if getter:
        return getter(key, default)
    value = params.get_param(key, default)
    normalized = str(value).strip().lower()
    if normalized in TRUE_VALUES:
        return True
    if normalized in FALSE_VALUES:
        return False
    return default

def set_string(params, key, value):
    setter = getattr(params, "set_str", None)
    if setter:
        return setter(key, value)
    return params.set_param(key, value)

def set_integer(params, key, value):
    setter = getattr(params, "set_int", None)
    if setter:
        return setter(key, value)
    return params.set_param(key, value)

def set_boolean(params, key, value):
    setter = getattr(params, "set_bool", None)
    if setter:
        return setter(key, value)
    return params.set_param(key, value)
