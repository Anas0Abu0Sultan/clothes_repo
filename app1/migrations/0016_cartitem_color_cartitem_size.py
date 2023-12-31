# Generated by Django 4.1.4 on 2023-07-20 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0015_remove_product_color_remove_product_size"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="color",
            field=models.CharField(
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
        migrations.AddField(
            model_name="cartitem",
            name="size",
            field=models.CharField(
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
    ]
