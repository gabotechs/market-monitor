from .flatten_dict import flatten_dict


def test_flatten_dict():
    r = flatten_dict({
        "a": {
            "b": 1
        },
        "c": 2
    })
    assert r["a.b"] == 1
    assert r["c"] == 2
