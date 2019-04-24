from django.contrib import admin
from .models import UserProfile, City, Country


class CountryAdmin(admin.ModelAdmin):
    list_display = (
         '__unicode__', 'country_name'
    )

    search_fields = (
        'country_name',
    )

class CityAdmin(admin.ModelAdmin):
    list_display = (
          '__str__', 'country', 'city_name'
    )

    search_fields = (
        'city_name',
    )

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'type', 'phone','address'
    )

    search_fields = (
        'user__username', 'user_type', 'phone',
    )


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Country,CountryAdmin)
admin.site.register(City,CityAdmin)
