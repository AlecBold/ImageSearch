from django import forms
from .models import *


class DataForm(forms.ModelForm):

    class Meta:
        model = DataModel
        fields = ['data_image']


class UserForm(forms.ModelForm):

    class Meta:
        model = UserModel
        fields = ['user_image']
