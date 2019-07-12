from django.forms import ModelForm


def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj


class OrgModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not hasattr(field, 'queryset'):
                continue
            model = field.queryset.model
            field.queryset = model.objects.all()


create_success_msg = "%(name)s was created successfully"
