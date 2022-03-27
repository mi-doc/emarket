from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)



from .models import Profile
User = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Incorrect login or password")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email has already been registered")
        return email


class EditProfileForm(forms.ModelForm):

    
    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].required = False
    
    class Meta:
        model = Profile
        exclude = ['user']

