from functools import wraps

from django.core.exceptions import PermissionDenied


def parent_required(view):
    """Allow only authenticated parent users; compose after login_required."""

    @wraps(view)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_parent:
            raise PermissionDenied
        return view(request, *args, **kwargs)

    return _wrapped
