import os
import uuid
from django.db import models
from students.models import Student

def get_payment_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"payment_{instance.student.nis}_{instance.month}_{instance.year}_{uuid.uuid4().hex[:8]}.{ext}"
    return os.path.join('payments/', new_filename)

class Payment(models.Model):
    STATUS_CHOICES = [
        ('menunggu', 'Menunggu Verifikasi'),
        ('lunas', 'Lunas'),
        ('ditolak', 'Ditolak'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    month = models.CharField(max_length=20, verbose_name="Bulan Pembayaran")
    year = models.IntegerField(verbose_name="Tahun")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Jumlah (Rp)")
    payment_proof = models.ImageField(upload_to=get_payment_upload_path, blank=True, null=True, verbose_name="Bukti Pembayaran")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'simapon_pembayaran_spp'

    def __str__(self):
        return f"SPP {self.student.name} - {self.month} {self.year}"


