from django import forms

from .models import Building


class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = (
            'name',
            'document_type',
            'document_number',
            'logo',
            'city',
            'address',
            'email',
            'mobile_phone',
            'phone_number',
            'initial_period',
        )
