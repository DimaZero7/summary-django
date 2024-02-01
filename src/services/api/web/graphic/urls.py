from django.urls import path

from services.api.web.graphic.views import GetGraphicDayView, GetGraphicMaxView

app_name = "graphic"

urlpatterns = [
    path("day/", GetGraphicDayView.as_view(), name="detail_day"),
    path("max/", GetGraphicMaxView.as_view(), name="detail_max"),
]
