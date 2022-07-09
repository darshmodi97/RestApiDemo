from rest_framework.permissions import BasePermission


class IsAllAccessible(BasePermission):
    """
    This is permission class will return true for all GET requests and for POST,PUT,DELETE method user have to login
    first otherwise it will return False and will show the error for "authentication credentials were not provided".
    """

    def __init__(self):
        self.message = "You have to login first."

    def has_permission(self, request, view):

        if request.method == "GET":
            print("in GET")
            return True
        else:
            print(request.user)
            if request.user.is_authenticated:
                return True
            else:
                return False
