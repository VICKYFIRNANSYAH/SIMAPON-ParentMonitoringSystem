from django.db import models
from students.models import Student

class Permit(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu Persetujuan'),
        ('disetujui', 'Disetujui'),
        ('ditolak', 'Ditolak'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='permits')
    reason = models.TextField(verbose_name="Alasan Izin")
    start_date = models.DateField(verbose_name="Tanggal Mulai")
    end_date = models.DateField(verbose_name="Tanggal Kembali")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Izin {self.student.name} ({self.start_date} - {self.end_date})"
