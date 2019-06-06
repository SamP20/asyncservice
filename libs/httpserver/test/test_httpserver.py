import pytest
from samp20.httpserver import normalize_path
from aiohttp import web


def test_normalize_path():
    path = "/abc/def"
    parts = normalize_path(path)
    assert parts == ["abc", "def"]

    path = "/abc/def/"
    with pytest.raises(web.HTTPMovedPermanently) as exc_info:
        normalize_path(path)
    assert exc_info.value.location == "/abc/def"

    path = "/abc/.././def"
    with pytest.raises(web.HTTPMovedPermanently) as exc_info:
        normalize_path(path)
    assert exc_info.value.location == "/def"

    path = "/./abc/../def/./"
    with pytest.raises(web.HTTPMovedPermanently) as exc_info:
        normalize_path(path)
    assert exc_info.value.location == "/def"

    path = "/abc/../../.."
    with pytest.raises(web.HTTPMovedPermanently) as exc_info:
        normalize_path(path)
    assert exc_info.value.location == "/"

    path = "/abc/..//../../..//"
    with pytest.raises(web.HTTPMovedPermanently) as exc_info:
        normalize_path(path)
    assert exc_info.value.location == "/"
