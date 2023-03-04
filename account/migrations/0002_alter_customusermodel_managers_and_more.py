# Generated by Django 4.1.5 on 2023-03-04 17:25

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="customusermodel",
            managers=[
                ("objects", account.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name="customusermodel",
            name="username",
        ),
        migrations.AlterField(
            model_name="customusermodel",
            name="first_name",
            field=models.CharField(max_length=150, verbose_name="first name"),
        ),
        migrations.AlterField(
            model_name="customusermodel",
            name="last_name",
            field=models.CharField(max_length=150, verbose_name="last name"),
        ),
    ]
