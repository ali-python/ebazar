# Generated by Django 2.1.7 on 2019-06-01 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='cash_on_delivery',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='support_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='invoice',
            name='transport_status',
            field=models.BooleanField(default=False),
        ),
    ]
