from django.urls import path

from services.api.web.graphic.views import (
    GetGraphicDayView,
    GetGraphicMaxView,
    GetGraphicWeekView,
)

app_name = "graphic"

urlpatterns = [
    path("day/", GetGraphicDayView.as_view(), name="detail_day"),
    path("week/", GetGraphicWeekView.as_view(), name="detail_week"),
    path("max/", GetGraphicMaxView.as_view(), name="detail_max"),
]
