from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import UserProfile, Task
from django.utils import timezone


class UserRegistrationForm(UserCreationForm):
    """Form for user registration - Question 3"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address'
    }))

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name'
    }))

    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name'
    }))

    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Phone number (optional)'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['username', 'email', 'first_name', 'last_name', 'phone']:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()
            # Save phone to profile if provided
            if self.cleaned_data['phone'] and hasattr(user, 'profile'):
                user.profile.phone = self.cleaned_data['phone']
                user.profile.save()

        return user


class UserLoginForm(AuthenticationForm):
    """Custom login form - Question 3"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'autofocus': True})


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile - Question 3"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'bio', 'birth_date']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields['email'].initial = self.user.email
            self.fields['first_name'].initial = self.user.first_name
            self.fields['last_name'].initial = self.user.last_name

    def save(self, commit=True):
        profile = super().save(commit=False)

        # Update related User fields
        if self.user:
            self.user.email = self.cleaned_data['email']
            self.user.first_name = self.cleaned_data['first_name']
            self.user.last_name = self.cleaned_data['last_name']
            if commit:
                self.user.save()

        if commit:
            profile.save()

        return profile


class TaskForm(forms.ModelForm):
    """Form for creating and updating tasks"""

    class Meta:
        model = Task
        fields = ['title', 'due_date', 'due_time', 'done']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Task title'
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'due_time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'form-control'
            }),
            'done': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }