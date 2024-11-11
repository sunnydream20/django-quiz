# quizzes/forms.py

from django import forms
from django.contrib.auth.models import User
from .models import UserPackage, Question

from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': 'Username must be letters and numbers only. ',  # Custom help text for the email field
        }
    

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = UserPackage
        fields = ['purchase_image']



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['option1', 'option2', 'option3', 'option4']  # adjust fields as necessary
        
