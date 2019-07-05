from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', "id": "title"}))
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control', "id": "file"}))


class FileFieldForm(forms.Form):
    file_field = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True, 'class': 'form-control'}))