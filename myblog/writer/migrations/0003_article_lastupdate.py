# Generated by Django 4.2.4 on 2023-08-28 05:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("writer", "0002_article_create_time_alter_user_last_login"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="lastupdate",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
