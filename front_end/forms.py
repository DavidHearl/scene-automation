from django import forms
from .models import Ship, Area

class ShipForm(forms.ModelForm):
    class Meta:
        model = Ship
        fields = ['name', 'contract_number', 'company']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = '__all__'
        widgets = {
            'status': forms.Select(choices=Area.STATUS_CHOICES),
            'priority': forms.Select(choices=Area.PRIORITY_CHOICES),
            'machine': forms.Select(choices=Area.AVAILABLE_MACHINES),
        }