from django.contrib import admin

from user.models import User


# Register your models here.
@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "created_at")
    readonly_fields = ("created_at",)
