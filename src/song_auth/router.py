from song_auth import views
from django.conf import settings
from django.conf.urls import include, url
from rest_framework import routers

router = routers.SimpleRouter(trailing_slash=False)
router.register("", views.SongsAuthenticationViewSet, basename="auth")
urlpatterns = [
    url(r"^", include(router.urls)),
]
