from django.db import models
from students.models import Student

class BehaviorNote(models.Model):
    CATEGORY_CHOICES = [
        ('prestasi', 'Prestasi'),
        ('pelanggaran', 'Pelanggaran'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='behavior_notes')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField(verbose_name="Deskripsi")
    points = models.IntegerField(verbose_name="Poin")
    date = models.DateField(auto_now_add=True, verbose_name="Tanggal")

    def __str__(self):
        return f"{self.category.capitalize()} - {self.student.name} ({self.points} Poin)"
