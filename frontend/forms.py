from django import forms 

from backend.models import Endpoint

class EndpointForm(forms.ModelForm):

    class Meta:
        model = Endpoint
        fields = [
            'name',
            'url',
            'description',
            'logo',
            # 'check_keyword',
            'user',
        ]
        widgets = {'user': forms.HiddenInput()}
