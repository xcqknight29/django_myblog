# Generated by Django 4.2.4 on 2023-08-28 05:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("writer", "0003_article_lastupdate"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="lastupdate",
            new_name="last_update",
        ),
    ]