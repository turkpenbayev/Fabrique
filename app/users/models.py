from decimal import Decimal
import random
import string
import datetime
import os
import uuid

from django.db import models
from django.db.models import Q, Sum, Count
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import MinValueValidator
from django.dispatch import receiver

# from .utils import number_generator, send_sms


class MyUserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('The username must be set')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = MyUserManager()

    def full_name(self,):
        return self.first_name + ' ' + self.last_name

    def __str__(self,):
        return f"{self.username} - {self.first_name} {self.last_name}"


class UserResponse(models.Model):
    """
        a response object is just a collection of questions and answers 
    """
    created = models.DateTimeField(auto_now_add=True)
    survey = models.ForeignKey(
        'surveys.Survey', on_delete=models.SET_NULL, null=True, blank=True)
    user_id = models.CharField("user unique identifier", max_length=36)
    is_anonymous = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.ForeignKey('surveys.Question', on_delete=models.CASCADE)
    response = models.ForeignKey(
        UserResponse, related_name="answers", on_delete=models.CASCADE)
    choices = models.ManyToManyField('surveys.Choice')
    text = models.TextField(blank=True, null=True)
