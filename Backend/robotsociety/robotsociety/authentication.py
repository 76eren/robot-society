from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
import re
import os
from cryptography.fernet import Fernet
class CookieJWTAuthentication(JWTAuthentication):


    def authenticate(self, request):
        header = self.get_header(request)
        print(f"Request headers: {request.headers}")
        print(f"Authorization header: {header}")

        raw_access_token = None
        raw_refresh_token = None

        if header is None:
            # Check if token exists in cookies
            cookie_header = request.headers.get('Cookie')
            if cookie_header:

                cookie_header = CookieJWTAuthentication.decrypt(cookie_header).replace(r"\073", ";")

                match = re.search(r'access=([^;]+); refresh=([^;]+)', cookie_header)

                if match:
                    raw_access_token = match.group(1)
                    raw_refresh_token = match.group(2)

            print(f"Access token from cookie: {raw_access_token}")
            print(f"Refresh token from cookie: {raw_refresh_token}")
        else:
            raw_access_token = self.get_raw_token(header)
            print(f"Access token from header: {raw_access_token}")

        if raw_access_token is None or raw_refresh_token is None or raw_refresh_token == "" or raw_access_token == "":
            return None

        try:
            validated_token = self.get_validated_token(raw_access_token)
        except Exception as e:
            return None

        return self.get_user(validated_token), validated_token

    @staticmethod
    def encrypt(value: str):
        encryption_key = os.environ.get('ENCRYPTION_PASSWORD')
        fernet = Fernet(encryption_key)
        return fernet.encrypt(value.encode()).decode()

    @staticmethod
    def decrypt(value: str):
        cookie_key = settings.SIMPLE_JWT["AUTH_COOKIE"]
        value = value.replace(f"{cookie_key}=", "")

        encryption_key = os.environ.get('ENCRYPTION_PASSWORD')
        fernet = Fernet(encryption_key)
        decrypted = fernet.decrypt(value.encode()).decode()
        decrypted = f"{cookie_key}={decrypted}"
        return decrypted
