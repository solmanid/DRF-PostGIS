from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from guardian.admin import GuardedModelAdmin

from .models import Accountant


# Register your models here.

@admin.register(Accountant)
class SupervisorAdmin(GuardedModelAdmin, UserAdmin):
    filter_horizontal = ('groups',)
    exclude = ('user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password')}),
        ('Role', {'fields': ('user_type', 'is_people', 'is_supervisor', 'is_accountant')}),
        ('Personal info',
         {'fields': ('username', 'last_login', 'date_joined', 'national_id', 'accountant_code', 'accountant_license')}),
        ('Groups', {'fields': ('groups',)}),
        ('Token', {'fields': ('token', 'refresh_token',)})
    )

    add_fieldsets = (
        (None, {'fields': ('email', 'is_staff',
                           'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('username', 'national_id', 'accountant_code', 'accountant_license',)}),
        ('Groups', {'fields': ('groups',)}),
    )
