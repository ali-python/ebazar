# Generated by Django 2.1.7 on 2019-04-01 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(blank=True, choices=[('Company', 'Company'), ('client', 'Client'), ('Corporate', 'Corporate')], default='Company', max_length=200, null=True),
        ),
    ]
