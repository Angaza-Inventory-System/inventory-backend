from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from backend.users.models import User
from .forms import UserCreationForm, UserChangeForm  

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm 

    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_superuser')

    search_fields = ('username', 'email', 'first_name', 'last_name')

    list_filter = ('is_superuser', 'role')

    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_superuser', 'permissions')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role'),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not change: 
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
