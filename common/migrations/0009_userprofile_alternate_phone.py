# Generated by Django 2.1.7 on 2019-05-13 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0008_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alternate_phone',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]