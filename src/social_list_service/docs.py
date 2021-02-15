from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Social list API",
        default_version="v1",
        description="""
            This app holds the Social Lists data for social me,
            as well as does the CRUD operations for them
        """,
        contact=openapi.Contact(email="developers@artistanbul.io"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
