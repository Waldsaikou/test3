# Generated by Django 4.2.2 on 2023-07-11 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0004_alter_seguimiento_table"),
    ]

    operations = [
        migrations.AddField(
            model_name="historial",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
    ]