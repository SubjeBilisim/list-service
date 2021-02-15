from django.contrib import admin
from django import forms

from .models import (
    SocialList,
    ListFollower,
)


class SocialListAdminForm(forms.ModelForm):
    class Meta:
        model = SocialList
        fields = "__all__"


class SocialListAdmin(admin.ModelAdmin):
    form = SocialListAdminForm
    list_display = [
        "picture",
        "last_updated",
        "created",
        "view_count",
    ]
    readonly_fields = [
        "picture",
        "last_updated",
        "created",
    ]


class ListFollowerAdminForm(forms.ModelForm):
    class Meta:
        model = ListFollower
        fields = "__all__"


class ListFollowerAdmin(admin.ModelAdmin):
    form = ListFollowerAdminForm



admin.site.register(ListFollower, ListFollowerAdmin)
admin.site.register(SocialList, SocialListAdmin)
