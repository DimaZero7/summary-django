from django.shortcuts import render


def graphic_view(request):
    return render(request, "graphic/graphic.html")
