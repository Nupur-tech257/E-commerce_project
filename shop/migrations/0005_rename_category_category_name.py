# Generated by Django 5.0.7 on 2024-07-28 05:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_category_product_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="category",
            new_name="name",
        ),
    ]
