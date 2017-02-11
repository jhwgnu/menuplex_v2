from django import forms
from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(label='Email', help_text='로그인 아이디로 사용할 이메일을 입력해주세요.',
            validators=[EmailValidator()])
    school = forms.CharField(required = True)


    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

    def save(self):
        user = super().save()
        school = self.cleaned_data['school']
        Profile.objects.create(user=user, school=school)
        return user


class LoginForm(AuthenticationForm):
    answer = forms.IntegerField(label='3+3=?')

    def clean_answer(self):
        answer = self.cleaned_data.get('answer', 0)
        if answer != 6:
            raise forms.ValidationError('땡~!!!')
        return answer

