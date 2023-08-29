# Generated by Django 4.2.4 on 2023-08-28 05:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("writer", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="create_time",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="user",
            name="last_login",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
