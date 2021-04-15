from rest_framework.permissions import BasePermission

from account.models import BlackListedToken


class IsTokenValid(BasePermission):
    """
    This permission class will check whether the JWT token is valid or not.
    """

    def __init__(self):
        self.message = "Session time out you have to login again."  # setting custom message.

    def has_permission(self, request, view):
        user_id = request.user.id
        is_allowed_user = True
        token = request.auth.decode("utf-8")
        try:
            is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
            if is_blackListed:
                is_allowed_user = False
        except BlackListedToken.DoesNotExist:
            is_allowed_user = True
        return is_allowed_user
