# Generated by Django 2.0.5 on 2018-07-09 22:30

import core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20180709_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=core.models.get_upload_to),
        ),
    ]
