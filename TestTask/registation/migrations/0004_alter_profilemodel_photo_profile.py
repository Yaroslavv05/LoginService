# Generated by Django 4.1.7 on 2023-03-29 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registation', '0003_alter_profilemodel_photo_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='photo_profile',
            field=models.ImageField(blank=True, null=True, upload_to='img/'),
        ),
    ]
