from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.translation import ugettext as _


class Country(models.Model):
    country_name=models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.country_name

class City(models.Model):
    country=models.ForeignKey(Country, on_delete=models.CASCADE,
                              related_name='country', null=True, blank=True)
    city_name=models.CharField(max_length=200, null=True, blank=True)

    def __unicode__(self):
        return self.country.country_name

class UserProfile(models.Model):
    USER_TYPE_COMPANY = 'Company'
    USER_TYPE_CLIENT = 'client'
    USER_TYPE_CORPORATE = 'Corporate'
    USER_TYPE_MERCHANT = 'Merchant'

    USER_TYPES = (
        (USER_TYPE_COMPANY, 'Company'),
        (USER_TYPE_CLIENT, 'Client'),
        (USER_TYPE_CORPORATE, 'Corporate'),
        (USER_TYPE_MERCHANT, 'Merchant'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    google_access_token = models.TextField(blank=True, null=True)
    facebook_profile_url = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_name = models.CharField(max_length=256, blank=True, null=True)
    profile_image = models.CharField(max_length=500, blank=True, null=True)
    is_custom_profile_image = models.BooleanField(default=False)
    phone = models.CharField(max_length=256, blank=True, null=True)
    alternate_phone=models.CharField(max_length=256, blank=True, null=True)
    gender = models.CharField(
        max_length=1, choices=(('m', _('Male')), ('f', _('Female'))),
        blank=True, null=True)
    type = models.CharField(
        max_length=200, choices=USER_TYPES, default=USER_TYPE_COMPANY,
        blank=True, null=True)
    hometown = models.CharField(max_length=256, blank=True, null=True)
    company_name = models.CharField(max_length=256, blank=True, null=True)
    location = models.CharField(max_length=256, blank=True, null=True)
    address=models.CharField(max_length=256, blank=True, null=True)
    city=models.ForeignKey(City, on_delete=models.CASCADE, related_name='user_city' , null=True, blank=True)

    def __unicode__(self):
        return self.user.username


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_feedback')
    comments=models.CharField(max_length=600, null=True, blank=True)

    def __unicode__(self):
        return self.user.username


# Signal Functions
def create_profile(sender, instance, created, **kwargs):
    """
    The functions used to check if user profile is not created
    and created the user profile without saving role and hospital
    :param sender:
    :param instance:
    :param created:
    :param kwargs:
    :return:
    """
    if created and not UserProfile.objects.filter(user=instance):
        return UserProfile.objects.create(
            user=instance
        )


# Signals
post_save.connect(create_profile, sender=User)
