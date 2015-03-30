from exam.models import *
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin


from exam.models import UserProfile
from exam.forms import UserChangeForm, UserCreationForm


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'date_and_time', 'rating', 'is_public')
    list_filter = ('author', 'category', 'date_and_time', 'rating', 'is_public')
    date_hierarchy = 'date_and_time'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'date_and_time', 'result')
    list_filter = ('user', 'test', 'date_and_time', 'result')
    date_hierarchy = 'date_and_time'


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    date_hierarchy = 'date_of_birth'
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'gender', 'country', 'city', 'address', 'institution', 'job', 'registration_date', 'rating', 'is_staff', 'is_superuser',)
    list_filter = ('gender', 'country', 'city', 'institution', 'job', 'registration_date', 'rating', 'is_superuser',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('last_name', 'first_name', 'middle_name', 'date_of_birth', 'gender', 'picture',)}),
        ('Address info', {'fields': ('country', 'city', 'address',)}),
        ('Profile info', {'fields': ('registration_date', 'rating',)}),
        ('Job info', {'fields': ('institution', 'job',)}),
        ('Permissions', {'fields': ('is_superuser', 'is_active',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

