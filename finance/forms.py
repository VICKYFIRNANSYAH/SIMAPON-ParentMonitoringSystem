from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    MONTH_CHOICES = [
        ('Januari', 'Januari'),
        ('Februari', 'Februari'),
        ('Maret', 'Maret'),
        ('April', 'April'),
        ('Mei', 'Mei'),
        ('Juni', 'Juni'),
        ('Juli', 'Juli'),
        ('Agustus', 'Agustus'),
        ('September', 'September'),
        ('Oktober', 'Oktober'),
        ('November', 'November'),
        ('Desember', 'Desember'),
    ]
    month = forms.ChoiceField(choices=MONTH_CHOICES, label="Bulan Pembayaran")

    class Meta:
        model = Payment
        fields = ['student', 'month', 'year', 'amount']
        widgets = {
            'year': forms.NumberInput(attrs={'min': 2000, 'max': 2100}),
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

class PaymentProofForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_proof']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_proof'].widget.attrs.setdefault('class', 'form-control')
