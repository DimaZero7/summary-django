from django.shortcuts import render


def graphic_day_view(request):
    return render(request, "graphic/day.html")


def graphic_max_view(request):
    return render(request, "graphic/max.html")
