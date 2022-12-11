from django.contrib.auth.models import AnonymousUser
from django.http import JsonResponse
from functools import wraps
from rest_framework.request import Request


def check_authenticated_user(inner_function):
    @wraps(inner_function)
    def wrapper(*args, **kwargs):
        for value in args:
            if type(value) == Request:
                if type(value.user) != AnonymousUser:
                    return inner_function(*args, **kwargs)
                return JsonResponse({"message": "Incorrect token passed"}, status=403)
            else:
                pass
    return wrapper
    