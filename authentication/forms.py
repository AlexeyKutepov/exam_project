__author__ = 'Alexey Kutepov'

from exam.models import UserProfile
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            'last_name',
            'first_name',
            'middle_name',
            'date_of_birth',
            'gender',
            'picture'
        )