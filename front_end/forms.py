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
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'ship-select'}),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['custom_ship_name'].required = False
        self.fields['custom_company'].required = False
        self.fields['custom_contract_number'].required = False

    def clean(self):
        cleaned_data = super().clean()
        selected_ship = cleaned_data.get('ship')

        if not selected_ship:
            # If "Create New Ship" is selected, check if any of the custom fields is empty
            for field_name in ['custom_ship_name', 'custom_company', 'custom_contract_number']:
                if not cleaned_data.get(field_name):
                    self.add_error(field_name, "This field is required when 'Create New Ship' is selected.")

        return cleaned_data
