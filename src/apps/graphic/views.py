from django.shortcuts import render


def graphic_day_view(request):
    return render(request, "graphic/day.html")


def graphic_week_view(request):
    return render(request, "graphic/week.html")


def graphic_month_view(request):
    return render(request, "graphic/month.html")


def graphic_max_view(request):
    return render(request, "graphic/max.html")
