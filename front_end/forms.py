from django import forms
from django.contrib.auth.models import User
from .models import Ship, Area, Machine, Booking


class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = '__all__'


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
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date', 'scanner', 'users']
