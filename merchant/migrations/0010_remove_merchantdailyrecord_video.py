# Generated by Django 2.1.7 on 2020-04-29 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0009_merchant_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merchantdailyrecord',
            name='video',
        ),
    ]
