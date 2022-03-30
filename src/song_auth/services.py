from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authtoken.models import Token
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from songs.services import BaseService

from songs.exceptions import SongsException

from song_auth.hashers import Hasher

from songs.errors import ValidationErr

from songs.settings import env

from song_auth.models import ForgotPasswordRequest


class SongsAuthService(BaseService):
    @classmethod
    def get_user(cls, pk: int, is_create=False) -> User:
        try:
            if pk:
                return User.objects.get(id=pk)
        except:
            pass
        return User() if is_create else None

    @classmethod
    def create_user(cls, validated_data: dict) -> User:
        try:
            raw_password = validated_data.get("password", "")
            password = Hasher.encode(
                raw_password, env("HASHID_FIELD_SALT")
            )
            validated_data.update(password=password)
            user = User(**validated_data)
            # define hook here
            user.save()
            return user
        except:
            pass
        return None

    @classmethod
    def log_in(cls, username="", email="", password=""):
        data: dict = {}
        try:
            if password and (email or username):
                ftr: Q = Q()
                if username:
                    ftr &= Q(username=username)
                else:
                    ftr &= Q(email=email)
                user = User.objects.get(ftr)
                if user:
                    hash_pass = Hasher.encode(
                        password, env("HASHID_FIELD_SALT")
                    )
                    from django.contrib.auth.hashers import make_password
                    make_password()
                    if user.password == hash_pass:
                        # make token return
                        payload = dict(
                            user_id=user.id,
                            exp=datetime.now() + timedelta(minutes=60),
                            iat=datetime.now()
                        )
                        token = jwt.encode(
                            payload,
                            env("SECRET_KEY"),
                            algorithm="HS256"
                        ).decode('utf-8')
                        data.update(
                            token=token,
                        )
        except:
            raise SongsException(error=ValidationErr.AUTHENTICATION_FAILED)
        return data


class ForgotPasswordRequestService(BaseService):
    @classmethod
    def get_forgot_request_password(cls, request_id: str = None, user: User = None):
        # required pk or user to get a forget request password object
        assert request_id or user
        request: ForgotPasswordRequest = None
        is_created = False
        try:
            if request_id:
                request = ForgotPasswordRequest.objects.get(id=request_id)
            elif user:
                request, is_created = ForgotPasswordRequest.objects.get_or_create(user=user)
        except Exception as e:
            pass
        if is_created:
            payload = dict(
                user_id=user.id,
                exp=datetime.now() + timedelta(minutes=60),
                iat=datetime.now()
            )
            token = jwt.encode(payload, env("SECRET_KEY"), "HS256").decode("utf-8")
            request.token = token
            request.save()
        return request

    @classmethod
    def get_forgot_password_reset_link(cls, forgot_pass_request: ForgotPasswordRequest):
        if not forgot_pass_request or forgot_pass_request.is_processed or forgot_pass_request.processed_at:
            return ""
        base_url = env("BASE_UI_FORGOT_PASSWORD_URL")
        return base_url.format(token=forgot_pass_request.id)

    @classmethod
    def verify_account_requested(cls, reset_request: ForgotPasswordRequest, verify_info: dict) -> dict:
        data: dict = {}
        try:
            token_data = jwt.decode(
                reset_request.token,
                key=env("SECRET_KEY"),
                verify=True,
                algorithms=["HS256"],
            )
            exp_time = datetime.fromtimestamp(int(token_data.get("exp")))
            if exp_time < datetime.now():
                raise SongsException(error=ValidationErr.REQUEST_RESET_TOKEN_EXPIRED)
            if getattr(reset_request.user, verify_info.get("key"), None) == verify_info.get("value"):
                data.update(
                    token=reset_request.token,
                    # todo get user information to view reset password page
                    user={}
                )
        except Exception as exception:
            if getattr(exception, "code") == ValidationErr.REQUEST_RESET_TOKEN_EXPIRED.get("code"):
                raise exception
        return data

    @classmethod
    def confirmed(cls, token: str, password: str, password2: str) -> bool:
        try:
            token_data = jwt.decode(
                token,
                key=env("SECRET_KEY"),
                verify=True,
                algorithms=["HS256"],
            )
            exp_time = datetime.fromtimestamp(int(token_data.get("exp")))
            if exp_time < datetime.now():
                raise SongsException(error=ValidationErr.REQUEST_RESET_TOKEN_EXPIRED)
            if password and password2 and (password == password2):
                password = Hasher.encode(password, env("HASHID_FIELD_SALT"))
                User.objects.filter(id=token_data.get("user_id")).update(password=password)
                return True
        except Exception:
            pass
        return False


