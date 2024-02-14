import random

from celery import shared_task

from apps.graphic.models import ChangeSharePrice


@shared_task(name="graphic.update_price")
def update_price_task() -> None:
    ChangeSharePrice.objects.create(changed_price=random.randint(1, 100))
