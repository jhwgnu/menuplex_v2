from django import forms

from food.models import Meal,Comment


class SoldOutForm(forms.ModelForm):
    class Meta:
        model = Meal
        fields = ['soldout']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']

