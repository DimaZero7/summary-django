from datetime import timedelta
from decimal import Decimal

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
        expected_result = []
        points_for_max = 3
        BuildGraphicService.POINTS_FOR_MAX = points_for_max

        # one point
        one_point_count = 3
        one_point_price = 10
        one_point_avg = one_point_price * one_point_count / one_point_count
        one_change_share_price_ids = []

        for iteration in range(one_point_count):
            change_share_price = ChangeSharePriceFactory(
                changed_price=one_point_price
            )
            one_change_share_price_ids.append(change_share_price.id)

            change_share_price.created_timestamp = (
                change_share_price.created_timestamp
                + timedelta(hours=iteration)
            )
            change_share_price.save(update_fields=["created_timestamp"])

        created_timestamp = (
            ChangeSharePrice.objects.filter(id__in=one_change_share_price_ids)
            .order_by("created_timestamp")
            .only("created_timestamp")
            .first()
            .created_timestamp
        )
        expected_result.append(
            {
                "created_timestamp": created_timestamp,
                "changed_price": round(
                    Decimal(one_point_avg), BuildGraphicService.DECIMAL_PLACES
                ),
            }
        )

        # two point
        two_point_count = 3
        two_point_price = 20
        two_point_avg = two_point_price * two_point_count / two_point_count
        two_change_share_price_ids = []

        for iteration in range(two_point_count):
            change_share_price = ChangeSharePriceFactory(
                changed_price=two_point_price
            )
            two_change_share_price_ids.append(change_share_price.id)

            change_share_price.created_timestamp = (
                change_share_price.created_timestamp
                + timedelta(hours=iteration + one_point_count)
            )
            change_share_price.save(update_fields=["created_timestamp"])

        created_timestamp = (
            ChangeSharePrice.objects.filter(id__in=two_change_share_price_ids)
            .order_by("created_timestamp")
            .only("created_timestamp")
            .first()
            .created_timestamp
        )
        expected_result.append(
            {
                "created_timestamp": created_timestamp,
                "changed_price": round(
                    Decimal(two_point_avg), BuildGraphicService.DECIMAL_PLACES
                ),
            }
        )

        # three point
        three_point_count = 2
        three_point_price = 30
        three_point_avg = (
            three_point_price * three_point_count / three_point_count
        )
        three_change_share_price_ids = []

        for iteration in range(three_point_count):
            change_share_price = ChangeSharePriceFactory(
                changed_price=three_point_price
            )
            three_change_share_price_ids.append(change_share_price.id)

            change_share_price.created_timestamp = (
                change_share_price.created_timestamp
                + timedelta(
                    hours=iteration + one_point_count + two_point_count
                )
            )
            change_share_price.save(update_fields=["created_timestamp"])

        created_timestamp = (
            ChangeSharePrice.objects.filter(
                id__in=three_change_share_price_ids
            )
            .order_by("created_timestamp")
            .only("created_timestamp")
            .first()
            .created_timestamp
        )
        expected_result.append(
            {
                "created_timestamp": created_timestamp,
                "changed_price": round(
                    Decimal(three_point_avg),
                    BuildGraphicService.DECIMAL_PLACES,
                ),
            }
        )

        # Action
        result = BuildGraphicService().get_max_graphic()

        # Check
        self.assertEqual(result, expected_result)

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
