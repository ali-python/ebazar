# Generated by Django 2.1.7 on 2019-04-20 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0005_merge_20190415_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
