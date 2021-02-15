from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication,
    TokenHasReadWriteScope,
)
from rest_framework import mixins, permissions, serializers, status, viewsets
from rest_framework.response import Response

import requests

from .models import (
    SocialList,
)
from .serializers import (
    SocialListSerializer,

)


class SocialListViewSet(viewsets.ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]


    queryset = SocialList.objects.all()
    serializer_class = SocialListSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = SocialList.objects.get(id=kwargs["list_id"])
        except ObjectDoesNotExist:
            return Response("No such list found", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = SocialList.objects.get(id=kwargs["list_id"])
        except ObjectDoesNotExist:
            return Response("No such list found", status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        try:
            instance = SocialList.objects.get(id=kwargs["list_id"])
        except ObjectDoesNotExist:
            return Response("No such list found", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
            