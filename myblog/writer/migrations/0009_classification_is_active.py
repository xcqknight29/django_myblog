# Generated by Django 4.2.4 on 2024-02-05 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("writer", "0008_alter_article_tag_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="classification",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]
