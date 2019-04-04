from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        '__unicode__', 'user', 'type',
    )

    search_fields = (
        'user__username', 'user_type',
    )


admin.site.register(UserProfile, UserProfileAdmin)