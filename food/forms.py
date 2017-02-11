from django import forms
from .models import Meal

class SoldOutForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['soldout']

