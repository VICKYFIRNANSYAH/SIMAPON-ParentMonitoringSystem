from django import forms
from .models import User
from students.models import Student

class ParentRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

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
        student_name = cleaned_data.get('student_name')
        student_grade = cleaned_data.get('student_grade')
        student_birth_date = cleaned_data.get('student_birth_date')

        if student_nis:
            student = Student.objects.filter(nis=student_nis).first()
            if not student:
                self.add_error('student_nis', "NIS tidak ditemukan. Pastikan santri sudah terdaftar.")
            else:
                if student.parent is not None:
                    self.add_error('student_nis', "Santri ini sudah terdaftar sebagai anak wali lain.")
                if student_name and student_name.strip().lower() != student.name.strip().lower():
                    self.add_error('student_name', "Nama santri tidak cocok dengan data existing.")
                if student_grade and student_grade.strip().lower() != student.grade.strip().lower():
                    self.add_error('student_grade', "Kelas santri tidak cocok dengan data existing.")
                if student_birth_date and student_birth_date != student.birth_date:
                    self.add_error('student_birth_date', "Tanggal lahir santri tidak cocok dengan data existing.")

        return cleaned_data

class GuruRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

class ImportFileForm(forms.Form):
    xlsx_file = forms.FileField(label="Upload Data (.xlsx/.csv)")
