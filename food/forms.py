from django import forms
from food.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['restaurant', 'author', 'content']

    def clean_restaurant(self):
        restaurant = self.cleaned_data.get('restaurant', '')
        return restaurant

    def clean_author(self):
        content = self.cleaned_data.get('author', '')
        return content

    def clean_content(self):
        content = self.cleaned_data.get('content', '')
        return content

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data


