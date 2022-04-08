import os

from django.db import models
from django.core.validators import FileExtensionValidator


def get_upload_path(instance, filename):
    name, ext = os.path.splitext(filename)
    return os.path.join(f'{str(instance.__class__.__name__).lower()}s', f'{name}{ext}')


class Checksum(models.Model):
    author = models.CharField(max_length=400)
    hash = models.CharField(db_index=True, max_length=128)
    doc = models.FileField(upload_to=get_upload_path, validators=[FileExtensionValidator(allowed_extensions=['txt'])])
    created_at= models.DateTimeField(auto_now_add=True)
