class URLHolder:
    def __init__(self, url):
        self.url = url


def _to_url_holder(val):
    if not val:
        return None
    # If it's already a URL string
    if isinstance(val, str) and (val.startswith('http://') or val.startswith('https://')):
        return URLHolder(val)
    # FieldFile-like
    try:
        name = getattr(val, 'name', None)
        if isinstance(name, str) and (name.startswith('http://') or name.startswith('https://')):
            return URLHolder(name)
    except Exception:
        return None
    return None


def ensure_user_image(request):
    """Context processor that exposes request.user_users_image_url as image object with .url
    so templates that render user.users.imageurl.url will work even when DB contains absolute URLs.
    """
    user_image = None
    try:
        if request.user and hasattr(request.user, 'users'):
            val = getattr(request.user.users, 'imageurl', None)
            user_image = _to_url_holder(val)
            if user_image:
                # attach a helper attribute so templates can use request.user_users_image_url.url
                return {'request_user_image': user_image}
    except Exception:
        pass
    return {'request_user_image': None}
