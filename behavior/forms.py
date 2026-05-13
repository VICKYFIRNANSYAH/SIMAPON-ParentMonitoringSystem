from django import forms
from .models import BehaviorNote
from students.models import Student

class BehaviorNoteForm(forms.ModelForm):
    class Meta:
        model = BehaviorNote
        fields = ['student', 'category', 'description', 'points']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
