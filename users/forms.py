from django import forms
from .models import User
from core.firebase_utils import find_siswa_by_nama_and_tgl_lahir

class WalimuridRegistrationForm(forms.ModelForm):
    nama_siswa = forms.CharField(max_length=150, required=True, label="Nama Lengkap Anak (Siswa)")
    tgl_lahir_siswa = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label="Tanggal Lahir Anak")
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Konfirmasi Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords tidak cocok.")

        nama_siswa = cleaned_data.get("nama_siswa")
        tgl_lahir_siswa = cleaned_data.get("tgl_lahir_siswa")

        if nama_siswa and tgl_lahir_siswa:
            # Check Firebase
            tgl_lahir_str = tgl_lahir_siswa.strftime('%Y-%m-%d')
            siswa = find_siswa_by_nama_and_tgl_lahir(nama_siswa, tgl_lahir_str)
            if not siswa:
                raise forms.ValidationError("Data anak tidak ditemukan di sistem. Pastikan nama dan tanggal lahir sesuai dengan yang didaftarkan oleh pihak pesantren.")
            else:
                self.siswa_id = siswa['id']
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.role = 'WALIMURID'
        user.siswa_id = getattr(self, 'siswa_id', None)
        if commit:
            user.save()
        return user
