# Generated by Django 4.1.4 on 2023-07-15 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0003_product_last_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="total_price_one_product",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
