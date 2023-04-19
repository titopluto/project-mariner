from django.contrib import admin

from .models import User


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "username",
        "family_name",
        "given_name",
    ]

    class Meta:
        model = User


admin.site.register(User, UserAdmin)
admin.site.site_header = "Mariner Website"
