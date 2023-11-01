from django import forms
from .models import Ship, Area


STATUS_CHOICES = [
    ("No Data", "No Data"),
    ("Legacy", "Legacy"),
    ("Failed", "Failed"),
    ("Queued", "Queued"),
    ("WIP", "WIP"),
    ("Completed", "Completed")
]


class AddItemForm(forms.Form):
    ship = forms.ModelChoiceField(
        queryset=Ship.objects.all(),
        required=False,
        empty_label="Create New Ship",
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    area_name = forms.CharField(max_length=100)

    # Fields for creating a new ship
    custom_ship_name = forms.CharField(max_length=200)
    custom_company = forms.CharField(max_length=200)
    custom_contract_number = forms.IntegerField()

    imported = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    processed = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    registered = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    aligned = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    cleaned = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    point_cloud = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    exported = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
    uploaded = forms.ChoiceField(choices=STATUS_CHOICES, initial="No Data")
