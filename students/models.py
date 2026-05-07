from django.db import models
from django.conf import settings

class Student(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children', limit_choices_to={'is_parent': True})
    nis = models.CharField(max_length=20, unique=True, verbose_name="NIS")
    name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    grade = models.CharField(max_length=50, verbose_name="Kelas")
    birth_date = models.DateField(verbose_name="Tanggal Lahir")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Foto Santri")

    def __str__(self):
        return f"{self.nis} - {self.name}"
