from typing import Dict, Any

from rest_framework import exceptions, status

from songs.errors import ValidationErr


class SongsException(exceptions.ValidationError):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    status_code = 400
    error: Dict[str, Any] = {}
    field: str = ""

    def __init__(self, error={"code": 0, "message": ""}, params=[], field="", status_code=400):
        self.error = {}
        if error["code"] == ValidationErr.SERVER_ERROR["code"]:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        elif error["code"] == ValidationErr.PARSE_ERROR["code"]:
            status_code = status.HTTP_400_BAD_REQUEST
        elif error["code"] == ValidationErr.AUTHENTICATION_FAILED["code"]:
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error["code"] == ValidationErr.NOT_AUTHENTICATED["code"]:
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error["code"] == ValidationErr.PERMISSION_DENIED["code"]:
            status_code = status.HTTP_403_FORBIDDEN
        elif error["code"] == ValidationErr.NOT_FOUND["code"]:
            status_code = status.HTTP_404_NOT_FOUND
        elif error["code"] == ValidationErr.METHOD_NOT_ALLOWED["code"]:
            status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        elif error["code"] == ValidationErr.NOT_ACCEPTABLE["code"]:
            status_code = status.HTTP_406_NOT_ACCEPTABLE
        elif error["code"] == ValidationErr.CONFLICT["code"]:
            status_code = status.HTTP_409_CONFLICT
        elif error["code"] == ValidationErr.UNSUPPORTED_MEDIA_TYPE["code"]:
            status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
        elif error["code"] == ValidationErr.THROTTLED["code"]:
            status_code = status.HTTP_429_TOO_MANY_REQUESTS
        elif error["code"] == ValidationErr.BAD_HEADER_PARAMS["code"]:
            status_code = status.HTTP_400_BAD_REQUEST
        elif error["code"] == ValidationErr.TOKEN_EXPIRED["code"]:
            status_code = status.HTTP_400_BAD_REQUEST

        try:
            message = error["message"].format(*params)
        except:
            message = error["message"]

        super().__init__({"code": error["code"], "message": message, "field": field})
        self.status_code = status_code
        self.error["code"] = error["code"]
        self.error["message"] = str(message)
        self.field = field

    def __str__(self):
        return self.error["message"]


class SongsExceptions(Exception):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """

    status_code: int = 400
    errors: list = []

    def __init__(self, status_code=400, errors=None):
        self.errors = []
        errors = errors or []
        self.status_code = status_code
        for error in errors:
            if isinstance(error, SongsException):
                self.errors.append(error)
