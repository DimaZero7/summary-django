from django.urls import include, path

from services.api.swagger.views import LoginRequiredWebSchemaView
from services.api.web.graphic import urls as graphic_urls

app_name = "mobile"

urlpatterns = [
    path("swagger.yaml", LoginRequiredWebSchemaView.without_ui()),
    path(
        "swagger/",
        LoginRequiredWebSchemaView.with_ui("swagger", cache_timeout=0),
    ),
    path(
        "graphic/",
        include(
            (graphic_urls.urlpatterns, graphic_urls.app_name),
            namespace="graphic",
        ),
    ),
    path(
        "test/",
        include(
            (graphic_urls.urlpatterns, graphic_urls.app_name),
            namespace="test",
        ),
    ),
]
