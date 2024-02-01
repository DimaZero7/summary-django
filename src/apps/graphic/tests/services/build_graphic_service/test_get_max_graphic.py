from datetime import datetime, timezone

from django.test import TestCase

from apps.graphic.models import ChangeSharePrice
from apps.graphic.services import BuildGraphicService
from apps.graphic.tests.factory import ChangeSharePriceFactory


class GetMaxGraphicTest(TestCase):
    def test_values_less_than_points(self):
        # Create data
        count = BuildGraphicService.POINTS_FOR_MAX - 1
        ChangeSharePriceFactory.create_batch(size=count)

        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertEqual(len(result), count)

    def test_values_more_than_points(self):
        # Create data
        count = BuildGraphicService.POINTS_FOR_MAX + 1
        ChangeSharePriceFactory.create_batch(size=count)

        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertEqual(len(result), BuildGraphicService.POINTS_FOR_MAX)

    def test_result_values(self):
        """
        The test checks:
            * Correct grouping of data by points
            * Immediate impact of new data points on the graph
            * Accuracy of distributing new points, especially when the total
                number of data points is unevenly divided by POINTS_FOR_MAX
            * Computation of the average price for each point
            * The created_timestamp for each point should be the smallest value
                in the group
        """
        # Create data
        points_for_max = 3
        BuildGraphicService.POINTS_FOR_MAX = points_for_max

        # one point
        one_point_count = 3
        one_point_price = 10
        one_point_avg = one_point_price * one_point_count / one_point_count
        one_points_data = [
            (one_point_price, datetime(2024, 1, 1, 1, tzinfo=timezone.utc)),
            (one_point_price, datetime(2024, 1, 1, 2, tzinfo=timezone.utc)),
            (one_point_price, datetime(2024, 1, 1, 3, tzinfo=timezone.utc)),
        ]
        for data in one_points_data:
            change_share_price = ChangeSharePrice.objects.create(
                changed_price=data[0]
            )
            change_share_price.created_timestamp = data[1]
            change_share_price.save(update_fields=["created_timestamp"])

        # two points
        two_point_count = 3
        two_point_price = 20
        two_point_avg = two_point_price * two_point_count / two_point_count
        two_points_data = [
            (two_point_price, datetime(2024, 1, 1, 4, tzinfo=timezone.utc)),
            (two_point_price, datetime(2024, 1, 1, 5, tzinfo=timezone.utc)),
            (two_point_price, datetime(2024, 1, 1, 6, tzinfo=timezone.utc)),
        ]
        for data in two_points_data:
            change_share_price = ChangeSharePrice.objects.create(
                changed_price=data[0]
            )
            change_share_price.created_timestamp = data[1]
            change_share_price.save(update_fields=["created_timestamp"])

        # three points
        three_point_count = 2
        three_point_price = 30
        three_point_avg = (
            three_point_price * three_point_count / three_point_count
        )
        three_points_data = [
            (three_point_price, datetime(2024, 1, 1, 7, tzinfo=timezone.utc)),
            (three_point_price, datetime(2024, 1, 1, 8, tzinfo=timezone.utc)),
        ]
        for data in three_points_data:
            change_share_price = ChangeSharePrice.objects.create(
                changed_price=data[0]
            )
            change_share_price.created_timestamp = data[1]
            change_share_price.save(update_fields=["created_timestamp"])

        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertEqual(result[0]["changed_price"], one_point_avg)
        self.assertEqual(result[1]["changed_price"], two_point_avg)
        self.assertEqual(result[2]["changed_price"], three_point_avg)

        self.assertEqual(result[0]["created_timestamp"], one_points_data[0][1])
        self.assertEqual(result[1]["created_timestamp"], two_points_data[0][1])
        self.assertEqual(
            result[2]["created_timestamp"], three_points_data[0][1]
        )

    def test_result_type(self):
        # Create data
        ChangeSharePriceFactory()

        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertIsInstance(result, list)
        self.assertIsInstance(result[0], dict)

    def test_result_type_dict_optional(self):
        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
