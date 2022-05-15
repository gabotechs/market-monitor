def flatten_dict(d: dict) -> dict:
    result = {}

    def f(root: dict, key=None):
        for k, v in root.items():
            new_k = f"{key}.{k}" if key is not None else k
            if type(v) == dict:
                f(v, new_k)
            elif type(v) == int or type(v) == float or type(v) == str:
                result[new_k] = v

    f(d)
    return result
