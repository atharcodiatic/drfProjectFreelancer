from django.contrib import admin

# Register your models here.

from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *

class CustomUserAdmin(UserAdmin):
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "is_staff", "is_active",'gender')
    list_filter = ("email", "is_staff", "is_active")

    ''' fieldsets - change user '''
    fieldsets = (
        (None, {"fields": ("email", "password",'gender','profile_pic')}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )

    '''add_fieldsets - form to add user '''
    add_fieldsets = (
        (None, {
            "classes": ('wide',),
            "fields": (
                "email",'username', "password1", "password2",'gender','profile_pic','pin_code', "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )
    search_fields = ('email','gender',)
    ordering = ("gender",)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Client)
admin.site.register(Freelancer)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(SelfSkill)