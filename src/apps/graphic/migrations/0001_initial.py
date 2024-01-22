# Generated by Django 5.0.1 on 2024-01-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ChangeSharePrice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "changed_price",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=9,
                        verbose_name="change price",
                    ),
                ),
                (
                    "created_timestamp",
                    models.DateTimeField(verbose_name="created timestamp"),
                ),
            ],
            options={
                "verbose_name": "change share price",
                "verbose_name_plural": "change shares price",
            },
        ),
    ]
