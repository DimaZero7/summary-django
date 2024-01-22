from rest_framework import serializers

from apps.graphic.models import ChangeSharePrice


class GetGraphicMaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChangeSharePrice
        fields = ("changed_price", "created_timestamp")
