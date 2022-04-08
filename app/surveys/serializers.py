from rest_framework import serializers
from .models import Checksum


class ChecksumSerializer(serializers.ModelSerializer):

    class Meta:
        model = Checksum
        fields = ('author', 'doc')


class ChecksumReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Checksum
        fields = ('hash', 'author', 'created_at')
        read_only_fields = fields
