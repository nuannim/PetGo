from urllib.parse import urlparse
from django.conf import settings
import os


class URLHolder:
    def __init__(self, url):
        self.url = url


def _to_public_path(u: str) -> str:
    """Convert an absolute storage URL to a public path served by Nginx.
    If input is already a path like /media/... return as-is.
    """
    if not u:
        return u
    try:
        # Case 1: '/media/http%3A/...' -> decode then use path
        if isinstance(u, str) and u.startswith('/media/') and '%3A' in u:
            from urllib.parse import unquote
            decoded = unquote(u[len('/media/'):])
            parsed = urlparse(decoded)
            if parsed.scheme in ('http', 'https') and parsed.path:
                return parsed.path
        # Case 2: '/media/http://...' or '/media/https://...' -> strip '/media/' then use path
        if isinstance(u, str) and (u.startswith('/media/http://') or u.startswith('/media/https://')):
            inner = u[len('/media/'):]
            parsed = urlparse(inner)
            if parsed.scheme in ('http', 'https') and parsed.path:
                return parsed.path
        # Case 3: 'media/http://...' or 'media/https://...' -> normalize then use path
        if isinstance(u, str) and (u.startswith('media/http://') or u.startswith('media/https://')):
            inner = '/' + u
            inner = inner[len('/media/'):]
            parsed = urlparse(inner)
            if parsed.scheme in ('http', 'https') and parsed.path:
                return parsed.path
        # If already a public path
        if u.startswith('/media/') or u.startswith('media/'):
            return u if u.startswith('/') else '/' + u
        parsed = urlparse(u)
        if parsed.scheme in ('http', 'https') and parsed.path:
            return parsed.path
    except Exception:
        pass
    return u


def _to_url_holder(val):
    if not val:
        return None
    # If it's a URL string or a media path
    if isinstance(val, str):
        return URLHolder(_ensure_served_url(_to_public_path(val)))
    # Some FieldFile expose .url; prefer it so MEDIA_URL is preserved
    try:
        url = getattr(val, 'url', None)
        if isinstance(url, str):
            return URLHolder(_ensure_served_url(_to_public_path(url)))
    except Exception:
        pass
    # FieldFile-like: only use .name when it's an absolute URL
    try:
        name = getattr(val, 'name', None)
        if isinstance(name, str) and (
            name.startswith('http://') or name.startswith('https://') or
            name.startswith('/media/http') or name.startswith('media/http')
        ):
            return URLHolder(_ensure_served_url(_to_public_path(name)))
    except Exception:
        return None
    return None

# Helper: ensure the URL is actually served. If it points to /media but the file
# is not present in this app's MEDIA_ROOT (dev), rewrite to absolute storage URL.
def _ensure_served_url(u: str) -> str:
    try:
        if isinstance(u, str) and (u.startswith('/media/') or u.startswith('media/')):
            path = u if u.startswith('/') else '/' + u
            rel = path[len('/media/'):]
            local_path = os.path.join(settings.MEDIA_ROOT, rel.replace('/', os.sep))
            storage_base = os.environ.get("STORAGE_API_URL", "http://127.0.0.1:8001").rstrip('/')
            if not os.path.exists(local_path) and storage_base:
                return f"{storage_base}{path}"
    except Exception:
        pass
    return u


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
