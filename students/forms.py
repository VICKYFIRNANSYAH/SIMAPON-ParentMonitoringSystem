from django import forms
from .models import Student
from users.models import User

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['parent', 'nis', 'name', 'grade', 'birth_date', 'photo']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].queryset = User.objects.filter(is_parent=True)
