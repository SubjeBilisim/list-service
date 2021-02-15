import os
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import force_authenticate

from . import api
from .models import (
    ListFollower,
    SocialList,
)
from .views import ViewCountView,ListFollowingView

api.SocialListViewSet.permission_classes = ()
ViewCountView.permission_classes=()
ListFollowingView.permission_classes=()
class SocialListTests(APITestCase):
    def test_create_list_crud(self):
        data={
        "created_by_id": 1}
        res_create=self.client.post("/social/list/",data=data)
        self.assertEqual(201,res_create.status_code)
        self.assertEqual(1,SocialList.objects.get(created_by_id=1).id)
        res_delete=self.client.delete("/social/list/1/")
        self.assertEqual(204,res_delete.status_code)
        self.assertEqual([],list(SocialList.objects.filter(created_by_id=1).values_list("id")))

    def test_view_count(self):
        data={
        "created_by_id": 1}
        res_create=self.client.post("/social/list/",data=data)
        self.assertEqual(201,res_create.status_code)
        res_view_count_increment=self.client.post("/social/list/view/count/2/")
        self.assertEqual("+1",res_view_count_increment.json())
        self.assertEqual(200,res_view_count_increment.status_code)

        res_view_count_view=self.client.get("/social/list/view/count/2/")
        self.assertEqual(1,res_view_count_view.json()[0]["view_count"])
        for i in range(10):
            self.client.post("/social/list/view/count/2/")
        res_view_count_view=self.client.get("/social/list/view/count/2/")
        self.assertEqual(11,res_view_count_view.json()[0]["view_count"])

