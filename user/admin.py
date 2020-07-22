from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


# Custom UserAdmin Doesn't work as of right now.
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserForm
#     form = CustomUserChangeForm
#     list_display = ('username', 'email')
#     class Meta:
#         model = CustomUser


admin.site.register(CustomUser, UserAdmin)