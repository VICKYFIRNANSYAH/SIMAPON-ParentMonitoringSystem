from django import forms
from .models import Permit

class PermitForm(forms.ModelForm):
    class Meta:
        model = Permit
        fields = ['student', 'reason', 'start_date', 'end_date', 'status']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 3}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')
