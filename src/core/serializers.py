from rest_framework import serializers

from .models import (
    SocialList,
    ListFollower,
)


class SocialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialList
        fields = ["last_updated", "created", "created_by_id"]







# social lists
class ListFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListFollower
        fields = ("list", "list_following_user", "created")


class ListFollowerFetchSerializer(serializers.Serializer):
    class Meta:
        model = ListFollower
        fields = ( "list_following_user", "created")

