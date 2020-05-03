# Generated by Django 2.1.7 on 2020-05-01 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0009_remove_order_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='customer_address',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='orderitem',
            name='item_description',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]