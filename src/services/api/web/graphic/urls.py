from django.urls import path

from services.api.web.graphic.views import GetGraphicMaxView

app_name = "graphic"

urlpatterns = [
    path("max/", GetGraphicMaxView.as_view(), name="detail_max"),
]
