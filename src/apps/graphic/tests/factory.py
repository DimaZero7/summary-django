import random

from factory import LazyAttribute
from factory.django import DjangoModelFactory

from apps.graphic.models import ChangeSharePrice


class ChangeSharePriceFactory(DjangoModelFactory):
    # Main fields
    changed_price = LazyAttribute(lambda o: random.randint(1, 1000))

    class Meta:
        model = ChangeSharePrice
