from django.urls import path

from apps.graphic.views import graphic_view

app_name = "graphic"

urlpatterns = [
    path("", graphic_view, name="graphic"),
]
