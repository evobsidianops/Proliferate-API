from django.contrib import admin
from django.urls import path, include

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from knox.auth import TokenAuthentication
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Pro API",
        default_version='v1',
        description="Onboarding, Registration, Login and Logout API Endpoints",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gisuekebho5880@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    validators=['ssv', 'flex'],
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=[TokenAuthentication],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('proliferate_app.urls')),
]

# Url patterns for API documentation
urlpatterns += [
    path('docs/', schema_view.without_ui(cache_timeout=None), name='schema-json'),
    path('docs/sg', schema_view.with_ui('swagger', cache_timeout=None), name='schema-swagger-ui'),
    path('docs/re', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc'),
]