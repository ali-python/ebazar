# Generated by Django 2.1.7 on 2020-05-04 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchant', '0015_auto_20200503_0024'),
    ]

    operations = [
        migrations.AddField(
            model_name='merchant',
            name='shop_image',
            field=models.ImageField(blank=True, null=True, upload_to='gallery'),
        ),
    ]