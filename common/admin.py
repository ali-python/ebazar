from django.contrib import admin
from .models import UserProfile, City, Country, Feedback


class CountryAdmin(admin.ModelAdmin):
    list_display = (
         '__unicode__', 'country_name'
    )

    search_fields = (
        'country_name',
    )

class CityAdmin(admin.ModelAdmin):
    list_display = (
          '__unicode__', 'country', 'city_name'
    )

    @staticmethod
    def country(obj):
        return obj.country.country_name

    search_fields = (
        'city_name',
    )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'type', 'phone', 'alternate_phone','address'
    )

    search_fields = (
        'user__username', 'user_type', 'phone','alternate_phone',
    )

class FeedBackAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'comments'
    )

    search_fields = (
        'user__username',
    )



admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Feedback, FeedBackAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(City,CityAdmin)
