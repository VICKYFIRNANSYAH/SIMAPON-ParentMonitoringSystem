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
        self.fields['parent'].required = False
        self.fields['photo'].required = False

class ImportStudentForm(forms.Form):
    xlsx_file = forms.FileField(label="Upload Data Santri (.xlsx/.csv)")
