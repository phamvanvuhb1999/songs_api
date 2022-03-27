from django.utils.translation import ugettext_lazy as _  # noqa


class Strings:
    SERVER_ERROR = {"code": 1000, "message": "A server error occurred."}
    PARSE_ERROR = {"code": 1001, "message": "Malformed request."}
    AUTHENTICATION_FAILED = {"code": 1002, "message": "Incorrect authentication credentials."}
    NOT_AUTHENTICATED = {"code": 1003, "message": "Authentication credentials were not provided."}
    PERMISSION_DENIED = {"code": 1004, "message": "You do not have permission to perform this action."}
    NOT_FOUND = {"code": 1005, "message": "{0} is not found."}
    METHOD_NOT_ALLOWED = {"code": 1006, "message": "Method not allowed."}
    NOT_ACCEPTABLE = {"code": 1007, "message": "Could not satisfy the request Accept header."}
    UNSUPPORTED_MEDIA_TYPE = {"code": 1008, "message": "Unsupported this media type in request."}
    THROTTLED = {"code": 1009, "message": "Request was throttled."}
    BAD_HEADER_PARAMS = {"code": 1010, "message": "Invalid request headers"}
    TOKEN_EXPIRED = {"code": 1011, "message": "Token expired"}
    UNEXPECTED_ERROR = {"code": 1012, "message": "{0}"}
    CUSTOM_EXCEPTION = {"code": 1013, "message": "{0}"}
    BAD_REQUEST = {"code": 1014, "message": "Bad request."}
    INVALID_REQUEST = {"code": 1015, "message": "Invalid request."}
    CONFLICT = {"code": 1016, "message": "{0} already exists"}
    DOES_NOT_SUPPORTED = {"code": 1018, "message": "This API does not support yet"}
    #
    REQUIRED = {"code": 1019, "message": "{0} is required."}
    INVALID_CONDITIONS = {"code": 1020, "message": "{0} is not satisfied with all conditions"}


ValidationErr = Strings
