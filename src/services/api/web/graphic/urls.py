from django.urls import path

from services.api.web.graphic.views import (
    GetGraphicDayView,
    GetGraphicMaxView,
    GetGraphicMonthView,
    GetGraphicWeekView,
)

app_name = "graphic"

urlpatterns = [
    path("day/", GetGraphicDayView.as_view(), name="detail_day"),
    path("week/", GetGraphicWeekView.as_view(), name="detail_week"),
    path("month/", GetGraphicMonthView.as_view(), name="detail_month"),
    path("max/", GetGraphicMaxView.as_view(), name="detail_max"),
]
