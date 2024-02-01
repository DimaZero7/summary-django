from django.urls import path

from apps.graphic.views import graphic_day_view, graphic_max_view

app_name = "graphic"

urlpatterns = [
    path("", graphic_day_view, name="day"),
    path("max/", graphic_max_view, name="max"),
]
