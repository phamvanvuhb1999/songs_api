import uuid

from django.contrib.auth.models import User
from django.db import models

from songs.models.base import TimeStampedModel

from datetime import datetime

from songs.models.base import UUIDModel


class ForgotPasswordRequest(TimeStampedModel, UUIDModel):
    processed_at = models.DateTimeField(null=True)
    is_processed = models.SmallIntegerField(default=0)
    token = models.CharField(max_length=254, null=True, unique=True)
    user = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL,
        db_column="user",
        unique=True
    )

    class Meta:
        db_table = "so_forget_password_request"


    @property
    def processed_time(self):
        return datetime.now() - self.processed_at
