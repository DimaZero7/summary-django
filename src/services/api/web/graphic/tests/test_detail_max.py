from decimal import Decimal
from unittest import mock

from django.urls import reverse_lazy
from rest_framework import status
from rest_framework.test import APITestCase

from apps.graphic.tests.factory import ChangeSharePriceFactory


class GetGraphicMaxTest(APITestCase):
    url = reverse_lazy("api:web:graphic:detail_max")

    def test_available_unauthorized(self):
        # Request
        response = self.client.get(self.url, format="json")

        # Check
        self.assertNotEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_result_fields(self):
        """
        Check that api:
            will return the expected number of fields
            will return the expected fields (name)
            will return the expected field type
        """
        # Creating data
        ChangeSharePriceFactory()

        expected_fields = {
            "changed_price": Decimal,
            "created_timestamp": str,
        }

        # Request
        response = self.client.get(self.url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(len(response.data[0]), len(expected_fields))
        for field in response.data[0]:
            self.assertIn(field, expected_fields)
            self.assertIsInstance(
                response.data[0][field],
                expected_fields[field],
            )

    def test_number_of_objects(self):
        # Create data
        count_obj = 2
        ChangeSharePriceFactory.create_batch(size=count_obj)

        # Request
        response = self.client.get(self.url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), count_obj)

    @mock.patch(
        "apps.graphic.services.BuildGraphicService.get_max_graphic",
        return_value={},
    )
    def test_result_data(self, fake_build_graphic):
        # Request
        response = self.client.get(self.url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(fake_build_graphic.called)
