from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from song_auth.serializers import AccountSerializer
from songs.views import GenericViewMixin

from song_auth.services import SongsAuthService
from songs.errors import ValidationErr
from songs.exceptions import SongsException

from song_auth.services import ForgotPasswordRequestService


class SongsAuthenticationViewSet(GenericViewMixin):
    view_set = "auth"
    serializer_class = AccountSerializer
    permission_classes = ()

    def retrieve(self, request, pk=0):
        """
            @apiVersion 1.0
            @api {GET} auth/:account_id Get account detail information
            @apiName DetailAccount
            @apiPermission authenticated, isAdmin
            @apiParam {Number} account_id Account Id
            @apiSuccess Account object
            @apiSuccessExample {json} Success-Response
            {
                "username": "username",
                "email": "email",
                "first_name": "first_name",
                "last_name": "last_name",
            }
        """
        user = None
        try:
            pk = int(pk)
            if pk:
                from django.contrib.auth.models import User
                user = User.objects.get(pk=pk)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        ret = dict(
            data=self.get_serializer(user).data,
        )
        return Response(ret, status=status.HTTP_200_OK)

    def list(self, request, pk=0):
        """
            @apiVersion 1.0
            @api {GET} auth Get account detail information
            @apiName DetailAccount
            @apiPermission authenticated, isAdmin
            @apiParam {Number} account_id Account Id
            @apiSuccess Account object
            @apiSuccessExample {json} Success-Response
            {
                "username": "username",
                "email": "email",
                "first_name": "first_name",
                "last_name": "last_name",
            }
        """
        user = None
        try:
            pk = int(pk)
            if pk:
                from django.contrib.auth.models import User
                user = User.objects.get(pk=pk)
        except:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        ret = dict(
            data=self.get_serializer(user).data,
        )
        return Response(ret, status=status.HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def signup(self, request):
        """
            @apiVersion 1.0
            @api {POST} auth/signup signup
            @apiName SignUp
            @apiPermission None
            @apiParam {Number} username User name
            @apiParam {Password} user password
            @apiSuccess Account object
            @apiSuccessExample {json} Success-Response
            {
                "username": "username",
                "email": "email",
                "first_name": "first_name",
                "last_name": "last_name",
            }
        """
        data = request.data.copy()
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Currently using jwt token view to get the access token
    # @action(detail=False, methods=['POST'])
    # def login(self, request):
    #     """
    #         @apiVersion 1.0
    #         @api {POST} auth/login SignIn
    #         @apiName SignIn
    #         @apiPermission None
    #         @apiAuthentication None
    #         @apiParam {Number} username User name
    #         @apiParam {Password} user password
    #         @apiSuccess Account object
    #         @apiSuccessExample {json} Success-Response
    #         {
    #             "token": "adfdajkfdhqjdlkfadasfdaf"
    #         }
    #     """
    #     data = request.data.copy()
    #     email = data.get("email")
    #     username = data.get("username")
    #     password = data.get("password")
    #     login_data = SongsAuthService.log_in(username, email, password)
    #     if login_data:
    #         return Response(login_data, status=status.HTTP_200_OK)
    #     raise SongsException(error=ValidationErr.AUTHENTICATION_FAILED)


class SongsResetPasswordViewSet(GenericViewMixin):
    view_set = "reset-password"
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
            @apiVersion 1.0
            @api {POST} auth/reset-password Forgot password
            @apiName ForgotPassword
            @apiPermission Authenticated
            @apiSuccessExample {json} Success-Response
            {
                "reset_password_token": "token_here_123123213"
            }
        """
        current_user = request.user
        if not current_user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        request_reset_pass = (
            ForgotPasswordRequestService.get_forgot_request_password(user=current_user)
        )
        request_reset_pass_link = ForgotPasswordRequestService.get_forgot_password_reset_link(request_reset_pass)
        # todo send url via email
        return Response(dict(reset_link=request_reset_pass_link), status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"])
    def confirmed(self, request):
        """
            @apiVersion 1.0
            @api {POST} auth/reset-password/confirmed Forgot password
            @apiName ForgotPassword
            @apiPermission Authenticated
            @apiSuccessExample {json} Success-Response
            {
                "success": True
            }
        """
        data = request.data.copy()
        if ForgotPasswordRequestService.confirmed(**data):
            return Response(dict(success=True), status=status.HTTP_200_OK)
        else:
            return Response(dict(success=False), status=status.HTTP_400_BAD_REQUEST)


class ResetPassConfirmationViewSet(GenericViewMixin):
    view_set = "reset-password-confirmation"
    serializer_class = None
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        """
            @apiVersion 1.0
            @api {POST} auth/reset-password-confirmation Forgot password
            @apiName ForgotPassword
            @apiPermission Authenticated
            @apiSuccessExample {json} Success-Response
            {
                "token": "afjafafaaaaaaaaaaaaaa",
                "user": {
                    "fullname": "vu",
                    "email": "phamvanvu@gmail.com",
                    "avatar": "https:google.com/image/avatar.png"
                }
            }
        """
        data = request.data.copy()
        email = data.get("email")
        username = data.get("username")
        reset_request_id = data.pop("request_id", None)

        reset_pass_request = ForgotPasswordRequestService.get_forgot_request_password(request_id=reset_request_id)
        if not (email or username) or not reset_pass_request:
            raise SongsException(error=ValidationErr.AUTHENTICATION_FAILED)
        value, key = (email, "email") if email else (username, "username")
        data = ForgotPasswordRequestService.verify_account_requested(reset_pass_request, {"key": key, "value": value})
        return Response(data, status=status.HTTP_200_OK)




