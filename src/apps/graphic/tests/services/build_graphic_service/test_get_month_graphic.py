from datetime import datetime, timedelta, timezone

from django.test import TestCase
from freezegun import freeze_time

from apps.graphic.models import ChangeSharePrice
from apps.graphic.services import BuildGraphicService
from apps.graphic.tests.factory import ChangeSharePriceFactory


class GetMonthGraphicTest(TestCase):
    def test_values_less_than_points(self):
        # Create data
        count = BuildGraphicService.POINTS_FOR_MONTH - 1
        change_shares_price = ChangeSharePriceFactory.create_batch(size=count)

        for iteration, change_share_price in enumerate(change_shares_price):
            change_share_price.created_timestamp -= timedelta(weeks=iteration)
            change_share_price.save(update_fields=["created_timestamp"])

        # Action
        result = BuildGraphicService().get_month_graphic()

        # Check
        self.assertEqual(len(result), count)

    def test_values_more_than_points(self):
        # Create data
        count = BuildGraphicService.POINTS_FOR_MONTH + 1
        change_shares_price = ChangeSharePriceFactory.create_batch(size=count, changed_price=455)

        for iteration, change_share_price in enumerate(change_shares_price):
            if iteration < BuildGraphicService.POINTS_FOR_MONTH:
                change_share_price.changed_price = 1
                change_share_price.created_timestamp -= timedelta(
                    weeks=iteration
                )
                change_share_price.save(update_fields=["created_timestamp", "changed_price"])

        # Action
        result = BuildGraphicService().get_month_graphic()

        # Check
        self.assertEqual(len(result), BuildGraphicService.POINTS_FOR_MONTH)

    @freeze_time(datetime(2024, 1, 7, 0, 0))
    def test_result_values(self):
        """
        The test checks:
            * Correct grouping of data by points
            * Average price calculation for each point
            * The created_timestamp for each point should be the smallest value
                in the group
        """
        # Create data
        # one point
        one_point_count = 2
        one_point_price = 10
        one_point_avg = one_point_price * one_point_count / one_point_count
        one_points_data = [
            (one_point_price, datetime(2024, 1, 1, 0, tzinfo=timezone.utc)),
            (
                one_point_price,
                datetime(2024, 1, 1, 1, tzinfo=timezone.utc),
            ),
        ]
        for data in one_points_data:
            change_share_price = ChangeSharePrice.objects.create(
                changed_price=data[0]
            )
            change_share_price.created_timestamp = data[1]
            change_share_price.save(update_fields=["created_timestamp"])

        # two point
        two_point_count = 3
        two_point_price = 20
        two_point_avg = two_point_price * two_point_count / two_point_count
        two_points_data = [
            (two_point_price, datetime(2024, 1, 2, 0, tzinfo=timezone.utc)),
            (
                two_point_price,
                datetime(2024, 1, 2, 1, tzinfo=timezone.utc),
            ),
            (
                two_point_price,
                datetime(2024, 1, 2, 2, tzinfo=timezone.utc),
            ),
        ]
        for data in two_points_data:
            change_share_price = ChangeSharePrice.objects.create(
                changed_price=data[0]
            )
            change_share_price.created_timestamp = data[1]
            change_share_price.save(update_fields=["created_timestamp"])

        # Action
        result = BuildGraphicService().get_week_graphic()

        # Check
        self.assertEqual(result[0]["changed_price"], one_point_avg)
        self.assertEqual(result[1]["changed_price"], two_point_avg)

        self.assertEqual(result[0]["created_timestamp"], one_points_data[0][1])
        self.assertEqual(result[1]["created_timestamp"], two_points_data[0][1])

    def test_result_type(self):
        # Create data
        ChangeSharePriceFactory()

        # Action
        result = BuildGraphicService().get_week_graphic()

        # Check
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

    def test_result_type_dict_optional(self):
        # Action
        result = BuildGraphicService().get_week_graphic()

        # Check
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
