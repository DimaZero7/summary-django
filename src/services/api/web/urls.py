from django.urls import path

from services.api.swagger.views import LoginRequiredWebSchemaView

app_name = "mobile"

urlpatterns = [
    path("swagger.yaml", LoginRequiredWebSchemaView.without_ui()),
    path(
        "swagger/",
        LoginRequiredWebSchemaView.with_ui("swagger", cache_timeout=0),
    ),
]
