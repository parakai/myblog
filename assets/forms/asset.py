from django import forms
from django.forms import ModelForm
from ..models.asset import Asset
from ..utils import OrgModelForm


class AssetCreateForm(ModelForm):
    class Meta:
        model = Asset
        fields = [
            'hostname', 'ip', 'os', 'port',  'comment', 'created_by',
            'nodes', 'is_formal', 'model', 'platform', 'appinfo', 'assettype',
            'cpu_model', 'cpu_count', 'cpu_cores', 'memory', 'disk_total'

        ]
        widgets = {
            'nodes': forms.Select(attrs={
                'class': 'select2', 'data-placeholder': 'Nodes'
            }),
            'port': forms.TextInput(),
        }
