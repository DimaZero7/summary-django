import random

from factory.django import DjangoModelFactory

from apps.graphic.models import ChangeSharePrice


class ChangeSharePriceFactory(DjangoModelFactory):
    # Main fields
    changed_price = random.randrange(1, 10000, 1)

    class Meta:
        model = ChangeSharePrice
