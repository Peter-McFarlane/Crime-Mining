from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'home'
urlpatterns = [
    path("", views.base, name = "base"),
    path("data/", views.data, name = "data"),
    path("findings/", views.findings, name = "findings"),
    path("docs/", views.docs, name = "docs"),
    path("view_pp", views.view_pp, name = "view_pp"),
    path("view_srs", views.view_srs, name = "view_srs"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)