# Generated by Django 4.2.2 on 2023-07-10 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="items_carrito",
            name="historial",
            field=models.BooleanField(default=False),
        ),
    ]
