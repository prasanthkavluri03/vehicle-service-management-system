from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

# Custom creation form incorporating extra fields
class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-select'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))
    address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('role', 'email', 'first_name', 'last_name', 'phone', 'address')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            existing_class = field.widget.attrs.get('class', '')
            if 'form-control' not in existing_class and 'form-select' not in existing_class:
                field.widget.attrs['class'] = f"{existing_class} form-control".strip()
            
            # Suppress verbose default help texts
            if field_name in ['username', 'password1', 'password2']:
                field.help_text = ""
            
            if field_name == 'username':
                field.widget.attrs['placeholder'] = 'Username'
            elif field_name == 'password1':
                field.widget.attrs['placeholder'] = 'Password'
            elif field_name == 'password2':
                field.widget.attrs['placeholder'] = 'Password confirmation'

    def full_clean(self):
        super().full_clean()
        for field_name, errors in self.errors.items():
            if field_name in self.fields:
                field = self.fields[field_name]
                existing_class = field.widget.attrs.get('class', '')
                if 'is-invalid' not in existing_class:
                    field.widget.attrs['class'] = f"{existing_class} is-invalid".strip()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data.get('role', 'customer')
        if commit:
            user.save()
        return user


# Form for updating user profiles
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
