from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    niveau_etude = forms.ChoiceField(choices=User._meta.get_field('niveau_etude').choices)
    classe = forms.CharField(max_length=50, required=False)
    ecole = forms.CharField(max_length=200, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'niveau_etude', 'classe', 'ecole']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.niveau_etude = self.cleaned_data['niveau_etude']
        user.classe = self.cleaned_data['classe']
        user.ecole = self.cleaned_data['ecole']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'niveau_etude', 'classe', 'ecole', 'date_naissance', 'avatar']

