# Generated by Django 2.1.7 on 2020-05-01 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0012_merchantdailyrecord_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchantsalesrecords',
            name='percent_ebazarr',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True),
        ),
    ]
