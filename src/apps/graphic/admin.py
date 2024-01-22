from django.contrib import admin
from rangefilter.filters import DateRangeFilter, NumericRangeFilter

from apps.graphic.models import ChangeSharePrice


@admin.register(ChangeSharePrice)
class ChangeSharePriceAdmin(admin.ModelAdmin):
    list_display = ("id", "changed_price", "created_timestamp")
    list_display_links = list_display

    list_filter = (
        ("changed_price", NumericRangeFilter),
        ("created_timestamp", DateRangeFilter),
    )
