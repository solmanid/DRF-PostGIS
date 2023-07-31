# Django Build-in
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Third Party
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

# Local Django
from accounts.models import OtpCode, User


@admin.register(User)
class UserAdmin(GuardedModelAdmin, UserAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    change_form_template = 'admin/user_detail.html'
    # list_display = ('image_preview',)
    fieldsets = (
        (None, {'fields': ('email', 'is_staff', 'is_superuser', 'password', 'avatar')}),
        ('Role', {'fields': ('user_type', 'is_people', 'is_supervisor', 'is_accountant')}),
        ('Personal info', {'fields': ('username', 'last_login', 'date_joined',)}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
        ('Token', {'fields': ('token', 'refresh_token',)})
    )

    def image_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50px" height="50px">', obj.avatar.url)
        return None

    image_preview.short_description = 'Avatar'

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'edit', 'delete']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f'{perm}_{model_name}' for perm in actions],
            klass=klass,
            any_perm=True
        )

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f"{action}_{opts.model_name}"
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'delete')

    def has_change_permission(self, request, obj=None):
        # return self.has_permission(request, obj, 'change')
        return super().has_change_permission(request)


@admin.register(OtpCode)
class OtpAdmin(admin.ModelAdmin):
    pass
