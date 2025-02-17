import re
from django import forms
from django.contrib.auth.models import User, Permission, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django import forms

class StyledFormMixin:
    """
    A mixin to apply Tailwind CSS styles to Django forms automatically.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print("Applying style mixin to form fields.")
        
        # Iterate over the fields in the form and update their widget attributes
        for field_name, field in self.fields.items():
            field_obj = self.fields[field_name]
            field_obj.widget.attrs.update(self.get_field_classes(field_obj))

    def get_field_classes(self, field):
        """
        Returns a dictionary of Tailwind CSS classes for each form field.
        """
        base_classes = "w-full px-4 py-2 border rounded-lg focus:ring focus:ring-blue-300"
        
        # Applying specific styles for each form widget type
        if isinstance(field.widget, forms.TextInput):
            field.widget.attrs.update({
                'class': base_classes,
            })
            # return {"class": f"{base_classes} border-gray-300 focus:border-blue-500"}
        
        if isinstance(field.widget, forms.EmailInput):
            return {"class": f"{base_classes} border-gray-300 focus:border-green-500"}
        
        if isinstance(field.widget, forms.PasswordInput):
            return {"class": f"{base_classes} border-gray-300 focus:border-red-500"}
        
        if isinstance(field.widget, forms.Textarea):
            return {"class": f"{base_classes} h-24 border-gray-300 focus:border-purple-500"}
        
        if isinstance(field.widget, forms.Select):
            return {"class": f"{base_classes} border-gray-300 focus:border-yellow-500"}
        
        # Default case: for fields not matching the specific widgets
        return {"class": base_classes}

class CustomRegistrationForm(StyledFormMixin, UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email = email).exists()

        if email_exists:
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []

        if len(password1) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password1):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password1):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password1):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password1):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password1
    
    def clean(self):  # non field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2= cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password do not match")

        return cleaned_data

class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreateGroupForm(StyledFormMixin, forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required= False,
        label = 'Assign Permission'
    )

    class Meta:
        model = Group
        fields = {"name", "permissions"}

class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label="Select a Role"
    )