from django.contrib import admin
from exam.models import *

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'birthday', 'gender', 'country', 'city', 'address', 'institution', 'job', 'registration_date', 'rating')
    list_filter = ('gender', 'country', 'city', 'institution', 'job', 'registration_date', 'rating')
    date_hierarchy = 'birthday'


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'category', 'date_and_time', 'rating')
    list_filter = ('author', 'category', 'date_and_time', 'rating')
    date_hierarchy = 'date_and_time'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'test', 'date_and_time', 'result')
    list_filter = ('user', 'test', 'date_and_time', 'result')
    date_hierarchy = 'date_and_time'



