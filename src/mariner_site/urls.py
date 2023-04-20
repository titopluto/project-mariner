"""mariner_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

from user import urls as user_urls
from permission import urls as permission_urls


urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api-schema",
        get_schema_view(
            title="API Schema", description="Guide for the Mariner Site API"
        ),
        name="api_schema",
    ),
    path(
        "api-docs",
        TemplateView.as_view(
            template_name="docs.html", extra_context={"schema_url": "api_schema"}
        ),
        name="swagger-ui",
    ),
]

# RestFramework URL
urlpatterns += [
    path("api/users/", include(user_urls)),
    path("api/permissions/", include(permission_urls)),
]
