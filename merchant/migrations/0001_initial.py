# Generated by Django 2.1.7 on 2019-04-06 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('phone', models.CharField(blank=True, max_length=200, null=True)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='MerchantDailyRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_time', models.DateTimeField(blank=True, null=True)),
                ('image_1', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='gallery')),
                ('video', models.FileField(blank=True, null=True, upload_to='gallery')),
                ('item_quantity', models.CharField(blank=True, max_length=200, null=True)),
                ('item_price', models.CharField(blank=True, max_length=200, null=True)),
                ('expiry', models.BooleanField(default=True)),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to='merchant.Merchant')),
            ],
        ),
        migrations.CreateModel(
            name='MerchantSalesRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_date', models.DateTimeField(blank=True, null=True)),
                ('purchased_quantity', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('purchased_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=65, null=True)),
                ('merchant_daily_record', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_records', to='merchant.MerchantDailyRecord')),
            ],
        ),
        migrations.CreateModel(
            name='MerchantUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='merchant_profile', to='merchant.Merchant')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_merchant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
