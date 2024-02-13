from rest_framework.response import Response
from rest_framework.views import APIView

from apps.graphic.services import BuildGraphicService
from services.api.web.graphic.serializers import (
    GetGraphicDaySerializer,
    GetGraphicMaxSerializer,
    GetGraphicWeekSerializer,
)


class GetGraphicDayView(APIView):
    permission_classes = ()
    response_serializer_class = GetGraphicDaySerializer

    def get(self, request, *args, **kwargs):
        data = BuildGraphicService().get_day_graphic()
        serializer = self.response_serializer_class(data, many=True)
        return Response(serializer.data)


class GetGraphicWeekView(APIView):
    permission_classes = ()
    response_serializer_class = GetGraphicWeekSerializer

    def get(self, request, *args, **kwargs):
        data = BuildGraphicService().get_week_graphic()
        serializer = self.response_serializer_class(data, many=True)
        return Response(serializer.data)


class GetGraphicMonthView(APIView):
    permission_classes = ()
    response_serializer_class = GetGraphicWeekSerializer

    def get(self, request, *args, **kwargs):
        data = BuildGraphicService().get_month_graphic()
        serializer = self.response_serializer_class(data, many=True)
        return Response(serializer.data)


class GetGraphicMaxView(APIView):
    permission_classes = ()
    response_serializer_class = GetGraphicMaxSerializer

    def get(self, request, *args, **kwargs):
        data = BuildGraphicService().get_max_graphic()
        serializer = self.response_serializer_class(data, many=True)
        return Response(serializer.data)
