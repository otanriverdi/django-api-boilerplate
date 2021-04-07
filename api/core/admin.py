from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            'fields': (
                'email',
                'password'
            ),
        }),
        (_('Personal Info'), {
            'fields': ('name',),
        }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser'
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login',),
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2'
            )
        }),
    )


class GroupAdminForm(forms.ModelForm):
    """
    ModelForm that adds an additional multiple select field for managing the users in the group.
    """
    users = forms.ModelMultipleChoiceField(
        get_user_model().objects.all(),
        widget=admin.widgets.FilteredSelectMultiple('Users', False),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            initial_users = self.instance.user_set.values_list('pk', flat=True)
            self.initial['users'] = initial_users

    def save(self, *args, **kwargs):
        kwargs['commit'] = True

        return super(GroupAdminForm, self).save(*args, **kwargs)

    def save_m2m(self):
        self.instance.user_set.clear()
        self.instance.user_set.add(*self.cleaned_data['users'])


class UpdatedGroupAdmin(GroupAdmin):
    """
    Customized GroupAdmin class that uses the customized form to allow management of users within a group.
    """
    form = GroupAdminForm


admin.site.register(models.User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, UpdatedGroupAdmin)
