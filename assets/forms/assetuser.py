from django.forms import ModelForm
from ..models.asset import AssetUser


class AssetUserUpdateForm(ModelForm):
    class Meta:
        model = AssetUser
        fields = ['is_admin', 'username', 'password']
