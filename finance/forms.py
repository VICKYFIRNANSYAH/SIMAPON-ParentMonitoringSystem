from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['student', 'month', 'year', 'amount']
        widgets = {
            'month': forms.TextInput(attrs={'placeholder': 'Januari, Februari, ...'}),
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_proof']
