import logging
import requests
import json

from django.db.models import F
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication,
    TokenHasReadWriteScope,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from .models import ListFollower, SocialList
from .serializers import (
    ListFollowSerializer,
    ListFollowerFetchSerializer,
    SocialListSerializer,
)

logger = logging.getLogger(__name__)




class ListFollowingView(APIView):
    #permission_classes = [TokenHasReadWriteScope]
    #authentication_classes = [OAuth2Authentication]
    permission_classes =()
    def post(self, request, *args, **kwargs):
        try:
            data = {
                "list": SocialList.objects.get(id=kwargs["list_id"]).id,
                "list_following_user": kwargs["user_id"]}
        except ObjectDoesNotExist:
            return Response(
                "No such user or social list found", status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ListFollowSerializer(data=data)
        if serializer.is_valid():
            try:
                serializer.save()
            except IntegrityError:
                return Response(
                    f"{kwargs['user_id']} already follows {kwargs['list_id']}",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

    def delete(self, request, *args, **kwargs):
        try:
            ListFollower.objects.get(
                list_following_user=kwargs["user_id"], list=kwargs["list_id"]
            ).delete()
        except ObjectDoesNotExist:
            return Response(
                "No such following found", status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            f"user {kwargs['user_id']} unfollowed {kwargs['list_id']}",
            status.HTTP_200_OK,
        )

    def get(self, request, *args, **kwargs):
        data = list(
                ListFollower.objects.filter(list=kwargs["list_id"]).values(
))
         # followers of a list
        serializer = ListFollowerFetchSerializer(data=data, many=True)
        try:
            if kwargs["user_id"] != "0":
                data = list(
                    SocialList.objects.filter(
                        created_by_id=kwargs["user_id"]
                    ).values("id", "created_by_id")
                )

                serializer = SocialListSerializer(data=data, many=True)
        except ObjectDoesNotExist:
            return Response(
                "User did not create any list", status=status.HTTP_400_BAD_REQUEST
            )
        if serializer.is_valid():
            return Response(serializer.initial_data, status=status.HTTP_200_OK)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

class ViewCountView(APIView):
    permission_classes = [TokenHasReadWriteScope]
    authentication_classes = [OAuth2Authentication]
    def post(self, request, *args, **kwargs):
        mylist=SocialList.objects.get(id=kwargs['list_id'])
        mylist.view_count = F('view_count') + 1
        mylist.save()
        return Response("+1",status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        mylist=SocialList.objects.filter(id=kwargs['list_id']).values()
        return Response(mylist,status=status.HTTP_200_OK)

               