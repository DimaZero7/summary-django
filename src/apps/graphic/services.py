import math
from typing import List, Optional

from django.db import connection

from apps.graphic.models import ChangeSharePrice


class BuildGraphicService:
    DECIMAL_PLACES = 3
    POINTS_FOR_MAX = 12

    def get_max_graphic(self) -> List[Optional[dict]]:
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
