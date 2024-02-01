import math
from datetime import datetime
from typing import Dict, List, Optional

from dateutil.relativedelta import relativedelta
from django.db import connection
from django.db.models import Avg
from django.utils import timezone

from apps.graphic.models import ChangeSharePrice


class BuildGraphicService:
    DECIMAL_PLACES = 3
    POINTS_FOR_DAY = 24
    POINTS_FOR_MAX = 12

    def get_day_graphic(self) -> List[Optional[Dict]]:
        current_timezone = timezone.get_current_timezone()
        time_limit = datetime.now(tz=current_timezone) - relativedelta(
            hours=self.POINTS_FOR_DAY
        )

        group_change_share_price = (
            ChangeSharePrice.objects.filter(
                created_timestamp__gte=time_limit,
            )
            .values(
                "created_timestamp__date",
                "created_timestamp__hour",
            )
            .annotate(
                price=Avg("changed_price"),
            )
            .order_by(
                "created_timestamp__date",
                "created_timestamp__hour",
            )
        )
        data = []
        for group in group_change_share_price:
            created_timestamp_date = group["created_timestamp__date"]
            created_timestamp = datetime(
                year=created_timestamp_date.year,
                month=created_timestamp_date.month,
                day=created_timestamp_date.day,
                hour=group["created_timestamp__hour"],
                tzinfo=current_timezone,
            )
            data.append(
                {
                    "created_timestamp": created_timestamp,
                    "changed_price": round(
                        group["price"], self.DECIMAL_PLACES
                    ),
                }
            )

        return data

    def get_max_graphic(self) -> List[Optional[Dict]]:
        change_share_price_count = ChangeSharePrice.objects.all().count()
        step = math.floor(change_share_price_count / self.POINTS_FOR_MAX)
        remainder = change_share_price_count % self.POINTS_FOR_MAX
        shift = 0
        groups = []

        for point in range(1, self.POINTS_FOR_MAX + 1):
            # remainder distribution
            if 1 <= remainder:
                shift += 1
                remainder -= 1

            groups.append(step * point + shift)

        condition_statements = "".join(
            [f"WHEN row <= {group} THEN {group} \n" for group in groups]
        )
        query = f"""
            WITH change_share_price as (
                SELECT
                    ROW_NUMBER() OVER (ORDER BY created_timestamp ASC) as row,
                    created_timestamp,
                    changed_price
                FROM graphic_changeshareprice
            )
            SELECT
                MIN(created_timestamp),
                AVG(changed_price),
                CASE
                    {condition_statements}
                END as point
            FROM change_share_price
            GROUP BY point
            ORDER BY point ASC
            """

        with connection.cursor() as cursor:
            cursor.execute(query, [groups])
            group_change_share_price = cursor.fetchall()

        data = []
        for group in group_change_share_price:
            data.append(
                {
                    "created_timestamp": group[0],
                    "changed_price": round(group[1], self.DECIMAL_PLACES),
                }
            )

        return data
