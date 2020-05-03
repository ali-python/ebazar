# Generated by Django 2.1.7 on 2019-04-18 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_auto_20190418_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_oder', to=settings.AUTH_USER_MODEL),
        ),
    ]
