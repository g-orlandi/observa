from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()

@admin.register(User)
class UserAdmin(AuthUserAdmin):
    list_display = list(AuthUserAdmin.list_display)[:] + ['plan']

    extra_fields = (
        ('Others', {'fields': ('profile_picture', 'plan')}),
    )
    fieldsets = AuthUserAdmin.fieldsets + extra_fields
    add_fieldsets = AuthUserAdmin.add_fieldsets + extra_fields

    def get_list_display(self, request):
        list_display = super(UserAdmin, self).get_list_display(request)[:]
        return list_display