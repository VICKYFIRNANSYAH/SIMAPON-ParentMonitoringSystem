import os
import uuid
from django.db import models
from django.conf import settings

def get_student_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    clean_name = "".join([c for c in instance.name if c.isalpha() or c.isdigit() or c in ('-', '_', ' ')]).rstrip().replace(' ', '_')
    new_filename = f"student_{instance.nis}_{clean_name}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('students/', new_filename)

class Student(models.Model):
    parent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='children', limit_choices_to={'is_parent': True}, blank=True, null=True)
    nis = models.CharField(max_length=20, unique=True, verbose_name="NIS")
    name = models.CharField(max_length=100, verbose_name="Nama Lengkap")
    grade = models.CharField(max_length=50, verbose_name="Kelas")
    birth_date = models.DateField(verbose_name="Tanggal Lahir")
    photo = models.ImageField(upload_to=get_student_upload_path, blank=True, null=True, verbose_name="Foto Santri")

    class Meta:
        db_table = 'simapon_santri'

    def __str__(self):
        return f"{self.nis} - {self.name}"


