from django.conf import settings
from rest_framework import serializers
from django.contrib.auth.models import User

from songs.errors import ValidationErr

from songs.exceptions import SongsException


class AccountSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(max_length=254, required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
        ]

    def validate_password(self, value):
        if not value:
            raise SongsException(error=ValidationErr.REQUIRED, params=["password"])

    def create(self, validated_data):
        from song_auth.services import SongsAuthService

        # validate password
        raw_password = self.initial_data.get("password")
        self.validate_password(raw_password)
        validated_data.update(password=raw_password)
        return SongsAuthService.create_user(validated_data)

    def update(self):
        super().save()
