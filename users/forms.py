from django import forms
from .models import User
from students.models import Student

class ParentRegistrationForm(forms.ModelForm):
    # Parent fields are in the User model
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")
    
    # Student fields
    student_nis = forms.CharField(max_length=20, label="NIS Anak")
    student_name = forms.CharField(max_length=100, label="Nama Lengkap Anak")
    student_grade = forms.CharField(max_length=50, label="Kelas Anak")
    student_birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Tanggal Lahir Anak")

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords tidak cocok.")
            
        student_nis = cleaned_data.get('student_nis')
        if Student.objects.filter(nis=student_nis).exists():
            self.add_error('student_nis', "NIS sudah terdaftar.")

        return cleaned_data
