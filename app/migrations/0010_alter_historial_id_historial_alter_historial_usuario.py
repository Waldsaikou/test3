# Generated by Django 4.2.2 on 2023-07-11 20:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("app", "0009_historial_usuario_alter_historial_id_historial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historial",
            name="id_historial",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="historial",
            name="usuario",
            field=models.ForeignKey(
                
                on_delete=django.db.models.deletion.SET_DEFAULT,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]