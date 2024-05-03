from django import forms
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
    class Meta:
        model = Booking
        fields = '__all__'
