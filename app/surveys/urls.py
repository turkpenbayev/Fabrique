from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('survey', SurveyViewSet, basename='survey')
router.register('question', QuestionViewSet, basename='question')

urlpatterns = router.urls