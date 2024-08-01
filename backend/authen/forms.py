from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm, UserChangeForm as BaseUserChangeForm
from backend.users.models import User

class UserCreationForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name', 'last_name')

class UserChangeForm(BaseUserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'first_name', 'last_name', 'is_superuser', 'permissions')
