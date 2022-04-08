from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status, mixins, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from drf_yasg.utils import swagger_auto_schema

from .utils import checksum_md5
from .serializers import ChecksumSerializer, ChecksumReadSerializer
from .models import Checksum


class ProtectViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ChecksumSerializer
    parser_classes=[MultiPartParser, FormParser]

    @swagger_auto_schema(responses={status.HTTP_200_OK: ChecksumReadSerializer})
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(hash='')
        hash_md5 = checksum_md5(instance.doc.path)
        instance.hash = hash_md5
        instance.save()
        if Checksum.objects.filter(Q(hash=hash_md5) & ~Q(pk=instance.pk)).exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(ChecksumReadSerializer(instance).data, status=status.HTTP_200_OK)
