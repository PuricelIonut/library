# Generated by Django 4.1.5 on 2023-02-26 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelf', '0007_alter_bookmodel_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmodel',
            name='image',
            field=models.ImageField(default='shelf/files/default/default_cover.jpg', upload_to='shelf/files/book-covers/'),
        ),
    ]
