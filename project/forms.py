from django import forms
from .models import Recipe
from django.contrib.auth import (
    authenticate,
    get_user_model
)
User = get_user_model()

class RecipeForm(forms.ModelForm):
    recipe_name = forms.CharField()
    recipe_steps = forms.CharField(widget=forms.TextInput())
    class Meta:
        model = Recipe
        exclude = ('recipe_user', 'frequency', 'last_used')

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username').lower()
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('User does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(label="Email Address")
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = [
            'email', 'username', 'password'
        ]
    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError(
                "This email is already being used"
            )
        return email
    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = User.objects.filter(username=username.lower())
        if username_qs.exists():
            raise forms.ValidationError(
                "This username is already being used"
            )
        return username
