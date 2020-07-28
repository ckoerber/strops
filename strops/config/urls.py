"""strops URL Configuration

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
import os

from django.urls import path, include

from django.contrib import admin
from django.contrib.auth import views as auth_views

from espressodb.management.utilities.settings import PROJECT_APPS
from espressodb.management.utilities.settings import ROOT_DIR

from rest_framework import routers

from strops.operators.rest.router import ROUTER as OP_ROUTER
from strops.schemes.rest.router import ROUTER as SCHEME_ROUTER


ROUTER = routers.DefaultRouter()
ROUTER.registry.extend(OP_ROUTER.registry)
ROUTER.registry.extend(SCHEME_ROUTER.registry)


urlpatterns = [
    path("", include("espressodb.base.urls", namespace="base")),
    path("admin/", admin.site.urls),
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        r"documentation/",
        include("espressodb.documentation.urls", namespace="documentation"),
    ),
    path(
        r"notifications/",
        include("espressodb.notifications.urls", namespace="notifications"),
    ),
    path(r"api/", include((ROUTER.urls, "api"), namespace="api")),
    path(r"api-auth/", include("rest_framework.urls")),
]

for app in PROJECT_APPS:
    url_file = os.path.join(ROOT_DIR, app.replace(".", "/"), "urls.py")
    if os.path.exists(url_file):
        _, app_name = app.split(".")
        if app_name == "config":
            continue
        urlpatterns.append(
            path(rf"{app_name}/", include(app + ".urls", namespace=app_name))
        )
