import urllib.parse


def is_safe_url(host_url, target):
    # Get the URL of the next page
    url = urllib.parse.urlparse(target)
    # Validate the URL
    # path starts w/ `/`
    path_starts_ok = url.path.startswith(
        # may be str or bytes
        "/"
        if isinstance(url.path, str)
        else b"/"
    )
    return path_starts_ok and (
        # is redirect w/o host
        not url.scheme
        # or host is same as current
        or url.scheme + "://" + url.netloc == host_url
    )
