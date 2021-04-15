from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User
from account.models import BlackListedToken

admin.site.unregister(User)  # unregistered auth user model from default fields.


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "last_login", "first_name", "last_name", "is_superuser")
    search_fields = ("username", "email", "first_name", "last_name",)
    readonly_fields = ("last_login",)


class BlackListedTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "timestamp", "token")


admin.site.register(User, UserAdmin)  # register again to show custom fields.
admin.site.register(BlackListedToken, BlackListedTokenAdmin)
