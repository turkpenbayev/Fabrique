from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework import serializers


from django.utils.translation import ugettext as _
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.models import BaseUserManager
from django.db import transaction

from .models import *
from surveys.models import Choice, Question


User = get_user_model()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=300, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    auth_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name', 'auth_token',)
        read_only_fields = ('id', 'auth_token')

    def get_auth_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class EmptySerializer(serializers.Serializer):
    pass


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    A user serializer for registering the user
    """

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name')

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError("username is already taken")
        return value

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError(
                'Current password does not match')
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value


class RequestPasswordResetSerializer(serializers.Serializer):
    """
    A user serializer for registering the user
    """
    username = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name',)


class AnswerCreateSerializer(serializers.ModelSerializer):
    choices = serializers.PrimaryKeyRelatedField(
        queryset=Choice.objects.all(), many=True)

    class Meta:
        model = Answer
        fields = ('question', 'choices', 'text')


class UserResponseCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(allow_blank=True, allow_null=True, required=False)
    answers = AnswerCreateSerializer(many=True, write_only=True)

    class Meta:
        model = UserResponse
        fields = ('id', 'survey', 'user_id', 'is_anonymous', 'answers')
        
    def validate(self, data):
        # The keys can be missing in partial updates
        if data["is_anonymous"]:
            if "user_id" not in data or data["user_id"]=="":
                raise serializers.ValidationError({
                    "user_id": "set user id if is_anonymous=true",
                })
                
        return super(UserResponseCreateSerializer, self).validate(data)

    def create(self, validated_data):
        try:
            answers = validated_data.pop('answers', [])
            with transaction.atomic():
                instance = UserResponse.objects.create(**validated_data)
                # bulk_create 
                for item in answers:
                    choices = item.pop('choices', [])
                    answer = Answer.objects.create(**item, response=instance)
                    answer.choices.add(*choices)
            return instance
        except Exception as ex:
            raise serializers.ValidationError(ex)
        

class AnswerSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField()
    question_type = serializers.IntegerField(source='question.question_type')

    class Meta:
        model = Answer
        fields = ('question', 'question_type','body')
        
    def get_body(self, obj):
        if obj.question.question_type == Question.TEXT:
            return obj.question.text
        else:
            return [choice.text for choice in obj.choices.all()]
        

class UserResponseSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    

    class Meta:
        model = UserResponse
        fields = ('id', 'survey', 'user_id', 'is_anonymous', 'answers')
