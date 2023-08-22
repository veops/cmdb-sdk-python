import hashlib


def build_api_key(key: str, secret: str, path: str, params: dict) -> dict:
    values = [ 
        str(params[k]) for k in sorted(params.keys())
        if (k not in ("_key", "_secret") and not isinstance(params[k], (dict, list)))
    ]
    values = "".join(values) or ""
    _secret = "".join([path, secret, values]).encode("utf-8")
    params["_secret"] = hashlib.sha1(_secret).hexdigest()
    params["_key"] = key
    return params
