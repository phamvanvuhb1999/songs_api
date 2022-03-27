from datetime import datetime, timedelta

import jwt
from django.contrib.auth.models import User
from django.db.models import Q
from songs.services import BaseService

from songs.exceptions import SongsException

from song_auth.hashers import Hasher

from songs.errors import ValidationErr

from songs.settings import env


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


