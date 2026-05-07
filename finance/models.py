from django.db import models
from students.models import Student

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
    payment_proof = models.ImageField(upload_to='payments/', blank=True, null=True, verbose_name="Bukti Pembayaran")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='menunggu')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SPP {self.student.name} - {self.month} {self.year}"
