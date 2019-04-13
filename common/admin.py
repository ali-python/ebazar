from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'type', 'phone'
    )

    search_fields = (
        'user__username', 'user_type', 'phone',
    )


admin.site.register(UserProfile, UserProfileAdmin)