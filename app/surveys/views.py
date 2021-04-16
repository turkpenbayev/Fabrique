from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from django.db.models import Prefetch, Q, Sum, Count

from .serializers import *
from .models import *


class SurveyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = SurveySerializer
    queryset = Survey.objects.all()
    http_method_names = ['get', 'post', 'delete', 'patch']
    serializer_classes = {
        'list': SurveySerializer,
        'retrieve': SurveyDetailSerializer,
        'create': SurveySerializer,
        'partial_update': SurveyUpdateSerializer,
        'destroy': SurveySerializer,
    }

    def get_queryset(self):
        queryset = self.queryset

        if self.action in ['retrieve']:
            queryset = queryset.prefetch_related(
                'questions', 'questions__choices')

        return queryset

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
    
    
class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().prefetch_related('choices')
    http_method_names = ['get', 'post', 'delete', 'patch']
