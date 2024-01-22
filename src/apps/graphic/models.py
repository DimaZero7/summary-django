from django.db import models
from django.utils.translation import gettext_lazy as _


class ChangeSharePrice(models.Model):
    """The model reflects the change in share price"""

    # Main fields
    changed_price = models.DecimalField(
        _("change price"), decimal_places=2, max_digits=9
    )
    created_timestamp = models.DateTimeField(
        _("created timestamp"),
        auto_now_add=True,
        auto_now=False,
    )

    class Meta:
        verbose_name = _("change share price")
        verbose_name_plural = _("change shares price")

    def __str__(self):
        return f"{self.id} | {self.changed_price}"
