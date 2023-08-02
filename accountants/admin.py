from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from guardian.admin import GuardedModelAdmin

from .models import Accountant, PaymentMark


# Register your models here.

@admin.register(Accountant)
class SupervisorAdmin(GuardedModelAdmin, UserAdmin):
    filter_horizontal = ('groups',)
    change_form_template = 'admin/user_detail.html'
    exclude = ('user_permissions',)
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password', 'avatar')}),
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

    def image_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50px" height="50px">', obj.avatar.url)
        return None

    image_preview.short_description = 'Avatar'


@admin.register(PaymentMark)
class PaymentMarkAdmin(admin.ModelAdmin):
    pass
