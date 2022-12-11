import ast
import time
from rest_framework import authentication
from rest_framework import exceptions

from authentication_app.models import AppUser
from authentication_app.utils.token_setup import authenticate_token
from taskbay.settings import BASE_URL


class UserTokenAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Bearer')
        request_url = request.build_absolute_uri()

        if request_url in [f"{BASE_URL}api/auth/signup/", f"{BASE_URL}api/auth/signin/"]:
            return None
        
        else:
            if not token:
                return None
            try:
                payload_bytes = authenticate_token(bytes(token, 'utf-8'))       
                if payload_bytes:
                    payload = ast.literal_eval(bytes.decode(payload_bytes))
                    current_time_in_seconds = time.time()
                    token_expiration_time = payload["exp"]
                    if token_expiration_time > current_time_in_seconds:
                        email = payload["email"]
                        user = AppUser.objects.get(email=email)
                        return (user, None)
                return None
            except AppUser.DoesNotExist:
                raise exceptions.AuthenticationFailed('Incorrect token with user field')
