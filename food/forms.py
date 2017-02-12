from django import forms

from food.models import Meal


class SoldOutForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['soldout']
