from django import forms
from django.contrib.auth.models import User
from .models import *


class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'contract_number', 'company', 'priority', 'image']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'status': forms.Select(choices=Area.STATUS_CHOICES),
            'priority': forms.Select(choices=Area.PRIORITY_CHOICES),
        }


class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ('currently_processing',)


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['ship', 'start_date', 'end_date', 'scanner']


class AreaPriorityForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['priority']
        widgets = {
            'priority': forms.Select(choices=Area.PRIORITY_CHOICES),
        }

class ShipPriorityForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['priority']
        widgets = {
            'priority': forms.Select(choices=Ship.PRIORITY_CHOICES),
        }
