# Generated by Django 4.2.4 on 2023-08-28 05:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("writer", "0004_rename_lastupdate_article_last_update"),
    ]

    operations = [
        migrations.RenameField(
            model_name="article",
            old_name="classification",
            new_name="classification_id",
        ),
    ]
