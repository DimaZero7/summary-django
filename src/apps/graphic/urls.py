from django.urls import path

from apps.graphic.views import (
    graphic_day_view,
    graphic_max_view,
    graphic_week_view,
)

app_name = "graphic"

urlpatterns = [
    path("", graphic_day_view, name="day"),
    path("week/", graphic_week_view, name="week"),
    path("max/", graphic_max_view, name="max"),
]
