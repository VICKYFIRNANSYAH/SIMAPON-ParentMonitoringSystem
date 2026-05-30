from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models import Q
from permits.models import Permit
from finance.models import Payment
from behavior.models import BehaviorNote
from .models import Notification

User = get_user_model()

@receiver(post_save, sender=Permit)
def permit_notification(sender, instance, created, **kwargs):
    if created:
        # Izin baru -> beritahu semua Admin dan Guru
        receivers = User.objects.filter(Q(is_admin=True) | Q(is_guru=True))
        for r in receivers:
            Notification.objects.create(
                user=r,
                title="Pengajuan Perizinan Baru",
                message=f"Santri {instance.student.name} mengajukan izin untuk alasan: '{instance.reason[:60]}...'",
                notification_type='perizinan',
                link="/dashboard/admin/permit/" if r.is_admin else "/dashboard/guru/"
            )
    else:
        # Status berubah -> beritahu Wali Murid (Parent)
        parent = instance.student.parent
        if parent:
            status_display = instance.get_status_display()
            Notification.objects.create(
                user=parent,
                title=f"Status Perizinan: {status_display}",
                message=f"Pengajuan perizinan {instance.student.name} untuk '{instance.reason[:50]}' telah dinyatakan {status_display.lower()}.",
                notification_type='perizinan',
                link="/dashboard/parent/"
            )

@receiver(post_save, sender=Payment)
def payment_notification(sender, instance, created, **kwargs):
    if created:
        # Tagihan baru dibuat oleh Admin -> beritahu Wali Murid (Parent)
        parent = instance.student.parent
        if parent:
            Notification.objects.create(
                user=parent,
                title="Tagihan SPP Baru",
                message=f"Tagihan SPP {instance.student.name} bulan {instance.month} {instance.year} sebesar Rp {instance.amount:,.0f} telah diterbitkan.",
                notification_type='keuangan',
                link="/dashboard/parent/"
            )
    else:
        # Ketika Wali Murid mengunggah bukti pembayaran (status berubah menjadi 'menunggu' dan bukti pembayaran ada)
        if instance.status == 'menunggu' and instance.payment_proof:
            admins = User.objects.filter(is_admin=True)
            for r in admins:
                Notification.objects.create(
                    user=r,
                    title="Bukti Pembayaran SPP Diunggah",
                    message=f"Wali Murid {instance.student.name} telah mengunggah bukti pembayaran SPP bulan {instance.month} {instance.year}.",
                    notification_type='keuangan',
                    link="/dashboard/admin/finance/"
                )
        
        # Ketika status pembayaran diubah oleh Admin (Lunas/Ditolak) -> beritahu Wali Murid (Parent)
        elif instance.status in ['lunas', 'ditolak']:
            parent = instance.student.parent
            if parent:
                status_display = instance.get_status_display()
                Notification.objects.create(
                    user=parent,
                    title=f"Status SPP: {status_display}",
                    message=f"Pembayaran SPP {instance.student.name} untuk bulan {instance.month} {instance.year} dinyatakan {status_display.lower()}.",
                    notification_type='keuangan',
                    link="/dashboard/parent/"
                )

@receiver(post_save, sender=BehaviorNote)
def behavior_notification(sender, instance, created, **kwargs):
    if created:
        parent = instance.student.parent
        if parent:
            cat_display = instance.get_category_display()
            Notification.objects.create(
                user=parent,
                title=f"Catatan Perilaku: {cat_display}",
                message=f"Santri {instance.student.name} mendapatkan catatan {cat_display.lower()} baru: '{instance.description[:60]}...' ({instance.points} Poin)",
                notification_type='perilaku',
                link="/dashboard/parent/"
            )
