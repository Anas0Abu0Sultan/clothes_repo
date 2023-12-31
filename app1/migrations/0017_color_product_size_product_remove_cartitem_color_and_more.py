# Generated by Django 4.1.4 on 2023-07-20 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0016_cartitem_color_cartitem_size"),
    ]

    operations = [
        migrations.CreateModel(
            name="color_product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "color",
                    models.CharField(
                        choices=[
                            ("", "Select Color"),
                            ("Black", "Black"),
                            ("White", "White"),
                            ("Red", "Red"),
                            ("Blue", "Blue"),
                            ("Green", "Green"),
                        ],
                        default="no_color",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="size_product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        choices=[
                            ("", "Select Size"),
                            ("XS", "XS"),
                            ("S", "S"),
                            ("M", "M"),
                            ("L", "L"),
                            ("XL", "XL"),
                        ],
                        default="no_size",
                        max_length=10,
                    ),
                ),
            ],
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="color",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="size",
        ),
    ]
