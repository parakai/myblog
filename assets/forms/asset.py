from django.forms import ModelForm
from django import forms
from ..models import Asset


class AssetCreateForm(ModelForm):
    class Meta:
        model = Asset
        fields = [
            'name', 'ip', 'os', 'port',  'comment', 'created_by',
            'nodes', 'is_formal', 'model', 'platform', 'appinfo', 'assettype'

        ]
        widgets = {
            'nodes': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': 'Nodes'
            }),
            'port': forms.TextInput(),
        }
