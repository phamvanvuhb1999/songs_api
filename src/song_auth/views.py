from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from song_auth.serializers import AccountSerializer
from songs.views import GenericViewMixin

from song_auth.services import SongsAuthService
from songs.errors import ValidationErr
from songs.exceptions import SongsException


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

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """
            @apiVersion 1.0
            @api {POST} auth/login SignIn
            @apiName SignIn
            @apiPermission None
            @apiParam {Number} username User name
            @apiParam {Password} user password
            @apiSuccess Account object
            @apiSuccessExample {json} Success-Response
            {
                "token": "adfdajkfdhqjdlkfadasfdaf"
            }
        """
        data = request.data.copy()
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")
        login_data = SongsAuthService.log_in(username, email, password)
        if login_data:
            return Response(login_data, status=status.HTTP_200_OK)
        raise SongsException(error=ValidationErr.AUTHENTICATION_FAILED)
