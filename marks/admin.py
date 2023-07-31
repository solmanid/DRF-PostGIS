# Django build-in
from django.contrib import admin
from django.contrib.gis.admin import TabularInline, StackedInline
# Third Party
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from leaflet.admin import LeafletGeoAdmin

# Local Django
from .models import PlacePoints, AcceptedPlace


# @admin.register(AcceptedPlace)
class AcceptedPlaceAdmin(StackedInline):
    model = AcceptedPlace
    extra = 1
    list_display = (
        'supervisor',
        'level',
        'created',
        'updated',
        'is_paid',
    )
    list_editable = (
        'level',
        'is_paid',
    )

    ordering = (
        'created',
    )


@admin.register(PlacePoints)
class LocationAdmin(GuardedModelAdmin, LeafletGeoAdmin):
    inlines = (AcceptedPlaceAdmin,)
    list_display = (
        'user',
        'status',
        'is_accepted',
        'likes'
    )
    list_editable = ('status', 'is_accepted')
    list_filter = ('status', 'is_accepted')
    ordering = ('-status', 'likes')
    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
    )

    def has_module_permission(self, request):
        if super().has_module_permission(request):
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request, action=None, klass: PlacePoints = None):
        opts = self.opts
        actions = [action] if action else ['view', 'change', 'delete', 'add']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name

        set_perm = get_objects_for_user(
            user=request.user,
            perms=[f'{perm}_{model_name}' for perm in actions],
            klass=klass,
            any_perm=True
        )

        return set_perm

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
