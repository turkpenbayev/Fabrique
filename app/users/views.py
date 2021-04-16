import json

from django.contrib.auth import get_user_model, logout
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.utils import timezone
from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Prefetch

from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.parsers import FormParser

from .serializers import *
from .utils import *
from .models import *

User = get_user_model()


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = EmptySerializer
    serializer_classes = {
        'login': UserLoginSerializer,
        'register': UserRegisterSerializer,
        'password_change': PasswordChangeSerializer,
    }

    @action(methods=['POST', ], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], detail=False)
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user_account(**serializer.validated_data)
        data = AuthUserSerializer(user).data
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(methods=['POST', ], detail=False)
    def logout(self, request):
        logout(request)
        data = {'success': 'Sucessfully logged out'}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated, ])
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()


class UserResponseViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = UserResponseSerializer
    queryset = UserResponse.objects.all()
    http_method_names = ['get', 'post', 'delete', ]
    serializer_classes = {
        'list': UserResponseSerializer,
        'retrieve': UserResponseSerializer,
        'create': UserResponseCreateSerializer,
        # 'destroy': SurveySerializer,
        # 'active_survey': SurveySerializer
    }

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured(
                "serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create']:
            # which is permissions.AllowAny
            self.permission_classes = [AllowAny]
        else:
            # which is permissions.IsAdminUser
            self.permission_classes = [IsAdminUser]

        return super(UserResponseViewSet, self).get_permissions()

    @action(methods=['get'], detail=False,
            permission_classes=[AllowAny, ],
            url_path='(?P<user_id>[^/.]+)',
            url_name='user_survey',)
    def user_id_survey(self, request, user_id=None):
        queryset = self.queryset.filter(user_id=user_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
