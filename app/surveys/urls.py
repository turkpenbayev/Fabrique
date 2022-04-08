from rest_framework import routers

from .views import ProtectViewSet

router = routers.DefaultRouter()
router.register('protect', ProtectViewSet, basename='protect')
urlpatterns = [*router.urls]