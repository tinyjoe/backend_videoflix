from rest_framework.permissions import BasePermission


class HasRefreshTokenCookie(BasePermission):
    """
    The `HasRefreshTokenCookie` class checks if the request contains a 'refresh' cookie.
    """
    def has_permission(self, request, view):
        return 'refresh' in request.COOKIES