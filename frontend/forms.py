from django import forms 

from backend.models import Endpoint

class EndpointForm(forms.ModelForm):

    class Meta:
        model = Endpoint
        fields = [
            'name',
            'description',
            'logo',
            'url',
            'user',
        ]
        widgets = {'user': forms.HiddenInput()}
