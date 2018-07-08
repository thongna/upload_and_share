# Generated by Django 2.0.5 on 2018-07-08 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20180627_0228'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(blank=True, default='', upload_to='documents/%Y/%m/%d/'),
        ),
    ]
