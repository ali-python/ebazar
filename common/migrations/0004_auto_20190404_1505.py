# Generated by Django 2.1.7 on 2019-04-04 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20190404_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(blank=True, choices=[('Company', 'Company'), ('client', 'Client'), ('Corporate', 'Corporate'), ('Merchant', 'Merchant')], default='Company', max_length=200, null=True),
        ),
    ]
