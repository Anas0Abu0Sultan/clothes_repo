# Generated by Django 4.1.4 on 2023-07-19 21:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0014_product_color_product_size"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="color",
        ),
        migrations.RemoveField(
            model_name="product",
            name="size",
        ),
    ]
