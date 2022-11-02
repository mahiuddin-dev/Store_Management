from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms

from .models import User


# class CustomUserCreationForm(UserCreationForm):
#     password1 = forms.CharField(label='Password',widget=forms.PasswordInput)
#     password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
#
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'email', 'password1','password2']
#
#         labels = {
#             'first_name': '',
#             'last_name': '',
#             'email': '',
#             'password1': '',
#             'password2': '',
#         }
#
#         widgets = {
#             'first_name': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': 'First Name', 'required': 'required'}),
#             'last_name': forms.TextInput(
#                 attrs={'class': 'form-control', 'placeholder': 'Last Name', 'required': 'required'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email', 'required': 'required'}),
#             'password1': forms.PasswordInput(
#                 attrs={'class': 'form-control', 'placeholder': 'Password', 'required': 'required'}),
#             'password2': forms.PasswordInput(
#                 attrs={'class': 'form-control', 'placeholder': 'Password', 'required': 'required'}),
#         }
#
#     def clean_email(self):
#         email = self.cleaned_data.get('email')
#         qs = User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Email is taken")
#         return email
#
#     def clean(self):
#         cleaned_data = super().clean()
#         password1 = cleaned_data.get("password1")
#         password2 = cleaned_data.get("password2")
#
#         if password1 is not None and password1 != password2:
#             self.add_error("password2", "Your passwords must match")
#         return cleaned_data
#
#     def save(self, commit=True):
#         # Save the provided password in hashed format
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         if commit:
#             user.save()
#         return user

class UserCreation(UserCreationForm):
    model = User
    fields = '__all__'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email',)

    def clean_password(self):
        return self.initial["password1"]
