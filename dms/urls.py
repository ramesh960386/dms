from django.conf import settings as se
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.schemas import get_schema_view as drf_schema
# drf_yasg code starts here
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="DMS API",
        default_version='v1',
        description="Welcome to the world of DMS",
        terms_of_service="https://www.myorbicular.co.in",
        contact=openapi.Contact(email="apptesting649@gmail.com"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
# ends here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dms_app.urls')),
    # swagger urls starts here
    re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(
        cache_timeout=0), name='schema-json'),
    path('doc/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    # api ends here
    path("openapi-schema/", drf_schema(
        title="Document Management System",
        description="API developers can use our service",
        url=None, version='v1'
    ))
]

if se.DEBUG:
    urlpatterns += static(se.MEDIA_URL, document_root=se.MEDIA_ROOT)
    urlpatterns += static(se.STATIC_URL, document_root=se.STATIC_ROOT)
