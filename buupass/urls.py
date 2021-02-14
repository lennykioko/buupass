"""buupass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework import routers, permissions
from rest_framework_simplejwt import views as jwt_views
from drf_yasg.views import get_schema_view  # noqa
from drf_yasg import openapi  # noqa

from authentication import views as auth_views

router = routers.DefaultRouter()
router.register(r'users', auth_views.UserViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Buupass API",
        default_version='v1',
        description="Demo API with RBAC",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="support@lenykioko.com"),
        license=openapi.License(name="ISC License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),  # noqa E501
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # noqa E501
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # noqa E501
    path('', include(router.urls)),
    path('', include('tickets.urls')),
    path('', include('authentication.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),  # noqa E501
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),   # noqa E501
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),  # noqa E501
    path('api/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),  # noqa E501
]
