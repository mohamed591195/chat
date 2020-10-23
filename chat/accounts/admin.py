from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserRegisterationForm, UserModificationForm


class UserAdmin(BaseUserAdmin):
    form = UserModificationForm
    add_form = UserRegisterationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (
            None,
            {
                'fields': ('email', 'password')
            }
        ),
        (
            'Personal info',
            {
                'fields': ('first_name', 'last_name', 'image', 'gender', 'bio')
            }
        ),
        (
            'Permissions',
            {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }
        ),
        # (
        #     'Important dates',
        #     {
        #         'fields': ('last_login', 'date_joined')
        #     }
        # ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
