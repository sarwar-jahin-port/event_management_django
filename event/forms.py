from django import forms
from django.utils import timezone
from event.models import Event, Category
from django.conf import settings
from django.apps import apps

User = apps.get_model(*settings.AUTH_USER_MODEL.split('.'))
class EventModelForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category', 'participants', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter event name'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter event description', 'rows': 4}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'location': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter event location'}),
            'category': forms.Select(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
            'image': forms.FileInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        }
    def clean_date(self):
        event_date = self.cleaned_data.get('date')
        if event_date < timezone.now().date():
            raise forms.ValidationError("The event date cannot be in the past.")
        return event_date

class CategoryModelForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter category name'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500', 'placeholder': 'Enter category description', 'rows': 4}),
        }

class RSVPForm(forms.Form):
    attending = forms.BooleanField(label="Attending?", required=False)