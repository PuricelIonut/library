# Generated by Django 4.1.5 on 2023-02-26 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0003_rename_name_bookmodel_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmodel',
            name='description',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]