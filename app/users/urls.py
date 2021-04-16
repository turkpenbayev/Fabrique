from rest_framework import routers

from django.urls import path

from .views import *

router = routers.DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
router.register('user-response', UserResponseViewSet, basename='user-response')

urlpatterns = router.urls
