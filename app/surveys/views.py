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
        'active_survey': SurveySerializer
    }

    def get_queryset(self):
        """
        if user not super admin return only active surveys

        """
        queryset = self.queryset

        if self.action in ['retrieve']:
            queryset = queryset.prefetch_related(
                'questions', 'questions__choices')

        user = self.request.user
        if not user.is_authenticated or not user.is_superuser:
            queryset = self.queryset.filter(end_date__gt=timezone.now())

        return queryset

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")
        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'create',]:
            # which is permissions.IsAdminUser
            self.permission_classes = [IsAdminUser]
        else:
            # which is permissions.AllowAny
            self.permission_classes = [AllowAny]

        return super(SurveyViewSet, self).get_permissions()

    @action(methods=['get'], detail=False,
            permission_classes=[AllowAny, ],
            url_path='active-survey',
            url_name='active_survey',)
    def active_survey(self, request):
        queryset = self.queryset.filter(end_date__gt=timezone.now())
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class QuestionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().prefetch_related('choices')
    http_method_names = ['get', 'post', 'delete', 'patch']
