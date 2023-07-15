# Generated by Django 4.1.4 on 2023-07-15 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0004_cartitem_total_price_one_product"),
    ]

    operations = [
        migrations.AddField(
            model_name="cartitem",
            name="total",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=9),
        ),
    ]
