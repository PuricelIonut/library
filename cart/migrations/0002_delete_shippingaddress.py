# Generated by Django 4.1.5 on 2023-04-04 12:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("cart", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="ShippingAddress",
        ),
    ]
