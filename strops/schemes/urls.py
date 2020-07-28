# pylint: disable=C0103
"""URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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
from django.urls import path
from strops.schemes import views

app_name = "schemes"
urlpatterns = [
    path("", views.ExpansionSchemeListView.as_view(), name="scheme-list"),
    path(
        "details/<int:pk>",
        views.ExpansionSchemeDetailsView.as_view(),
        name="expansion_scheme_detail",
    ),
    path(
        "operator-mapping/", views.mapping.IndexView.as_view(), name="operator-mapping"
    ),
    path(
        "operator-mapping/from/",
        views.mapping.PickSourceScaleView.as_view(),
        name="op-mapping-source-scale",
    ),
    path(
        "operator-mapping/from/<slug:source_scale>/to/",
        views.mapping.PickTargetScaleView.as_view(),
        name="op-mapping-target-scale",
    ),
    path(
        "operator-mapping/from/<slug:source_scale>/to/<slug:target_scale>/",
        views.mapping.PickBranchView.as_view(),
        name="op-mapping-branch-select",
    ),
    path(
        "operator-mapping/present/",
        views.mapping.PresentView.as_view(),
        name="op-mapping-present",
    ),
]
