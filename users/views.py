import csv
import io

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import ParentRegistrationForm, GuruRegistrationForm, ImportFileForm
from students.models import Student
from students.forms import StudentForm, ImportStudentForm
from users.models import User, Notification
from django.http import JsonResponse
from finance.models import Payment
from finance.forms import PaymentForm
from permits.models import Permit
from permits.forms import PermitForm
from behavior.forms import BehaviorNoteForm
from behavior.models import BehaviorNote
from .reports import AdminDashboardReport, GuruDashboardReport, ParentDashboardReport




def parse_import_file(uploaded_file):
    """
    Parse XLSX or CSV file dan convert semua nilai ke string.
    Mendukung berbagai format input (int, float, date, string).
    """
    filename = uploaded_file.name.lower()
    if filename.endswith('.csv'):
        decoded = uploaded_file.read().decode('utf-8')
        return list(csv.DictReader(io.StringIO(decoded)))

    if filename.endswith('.xlsx'):
        try:
            from openpyxl import load_workbook
            from datetime import datetime, date
        except ImportError:
            raise ImportError('openpyxl belum terpasang. Instal dengan pip install openpyxl.')

        workbook = load_workbook(uploaded_file, data_only=True)
        sheet = workbook.active
        rows = list(sheet.values)
        if not rows:
            return []

        headers = [str(cell).strip() if cell is not None else '' for cell in rows[0]]
        parsed = []
        for row in rows[1:]:
            row_data = {}
            for idx, header in enumerate(headers):
                if not header:
                    continue
                value = row[idx] if idx < len(row) else None
                
                # Convert semua jenis data ke string
                if value is None:
                    value = ''
                elif isinstance(value, (date, datetime)):
                    # Format tanggal ke DD/MM/YYYY
                    value = value.strftime('%d/%m/%Y')
                elif isinstance(value, (int, float)):
                    # Convert angka ke string, hapus desimal jika ada
                    if isinstance(value, float) and value.is_integer():
                        value = str(int(value))
                    else:
                        value = str(value)
                else:
                    value = str(value)
                
                # Strip whitespace
                if isinstance(value, str):
                    value = value.strip()
                
                row_data[header] = value
            parsed.append(row_data)
        return parsed

    raise ValueError('Format file tidak didukung. Gunakan .xlsx atau .csv')


def landing_page(request):
    return render(request, 'landing.html')


def register_parent(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_parent = True
            user.save()

            student = Student.objects.get(nis=form.cleaned_data['student_nis'])
            student.parent = user
            student.save()

            login(request, user)
            return redirect('dashboard')
    else:
        form = ParentRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def dashboard(request):
    if request.user.is_admin or request.user.is_staff:
        return redirect('admin_dashboard')
    elif request.user.is_guru:
        return redirect('guru_dashboard')
    elif request.user.is_parent:
        return redirect('parent_dashboard')
    else:
        return render(request, 'landing.html')


@login_required
def admin_dashboard(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    report = AdminDashboardReport(request.user)
    context = report.get_summary()
    return render(request, 'dashboards/admin/index.html', context)



@login_required
def guru_dashboard(request):
    if not request.user.is_guru:
        return redirect('dashboard')

    form = BehaviorNoteForm()
    if request.method == 'POST':
        if request.POST.get('submit_type') == 'behavior_note':
            form = BehaviorNoteForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Catatan sikap santri berhasil ditambahkan.')
                return redirect('guru_dashboard')
        else:
            permit_id = request.POST.get('permit_id')
            action = request.POST.get('action')
            if action in ['approve', 'reject'] and permit_id:
                try:
                    permit = Permit.objects.get(id=permit_id)
                    permit.status = 'disetujui' if action == 'approve' else 'ditolak'
                    permit.save()
                    messages.success(request, f'Permintaan izin {permit.student.name} berhasil diperbarui.')
                except Permit.DoesNotExist:
                    messages.error(request, 'Data izin tidak ditemukan.')
                return redirect('guru_dashboard')

    report = GuruDashboardReport(request.user)
    summary = report.get_summary()
    context = {
        'form': form,
        **summary,
        'permits': Permit.objects.all().select_related('student').order_by('-created_at')[:20],
        'behavior_notes': BehaviorNote.objects.all().select_related('student').order_by('-date', '-id')[:20],
    }
    return render(request, 'dashboards/guru/index.html', context)


@login_required
def parent_dashboard(request):
    children = request.user.children.all()

    if request.method == 'POST' and 'payment_id' in request.POST:
        payment_id = request.POST.get('payment_id')
        payment_proof = request.FILES.get('payment_proof')
        try:
            payment = Payment.objects.get(id=payment_id, student__parent=request.user)
            if payment_proof:
                payment.payment_proof = payment_proof
                payment.status = 'menunggu'
                payment.save()
                messages.success(request, 'Bukti pembayaran berhasil diunggah. Tunggu verifikasi admin.')
            else:
                messages.error(request, 'Mohon unggah bukti pembayaran berupa gambar.')
        except Payment.DoesNotExist:
                messages.error(request, 'Tagihan tidak ditemukan.')
        return redirect('parent_dashboard')

    if request.method == 'POST' and request.POST.get('submit_type') == 'permit_request':
        student_id = request.POST.get('student')
        reason = request.POST.get('reason')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        try:
            student = children.get(id=student_id)
            if not reason or not start_date or not end_date:
                messages.error(request, 'Mohon lengkapi semua data pengajuan izin.')
            else:
                Permit.objects.create(
                    student=student,
                    reason=reason,
                    start_date=start_date,
                    end_date=end_date,
                    status='menunggu',
                )
                messages.success(request, 'Pengajuan izin berhasil dikirim. Tunggu persetujuan guru/admin.')
        except Student.DoesNotExist:
            messages.error(request, 'Data anak tidak valid untuk pengajuan izin.')
        return redirect('parent_dashboard')

    report = ParentDashboardReport(request.user)
    context = report.get_summary()
    return render(request, 'dashboards/parent/index.html', context)


@login_required
def admin_guru_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    form = GuruRegistrationForm()
    import_form = ImportFileForm()

    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            guru_id = request.POST.get('guru_id')
            try:
                guru = User.objects.get(id=guru_id, is_guru=True)
                guru.delete()
                messages.success(request, 'Data Guru berhasil dihapus.')
            except User.DoesNotExist:
                messages.error(request, 'Data Guru tidak ditemukan.')
            return redirect('admin_guru_list')
        elif request.POST.get('submit_type') == 'import_guru':
            import_form = ImportFileForm(request.POST, request.FILES)
            if import_form.is_valid():
                try:
                    rows = parse_import_file(import_form.cleaned_data['xlsx_file'])
                    added = 0
                    skipped = 0
                    for row in rows:
                        username = (row.get('username') or row.get('Username') or '').strip()
                        email = (row.get('email') or row.get('Email') or '').strip()
                        phone_number = (row.get('phone_number') or row.get('Phone') or row.get('phone') or '').strip()
                        password = (row.get('password') or row.get('Password') or '').strip() or 'password123'
                        if not username or not email:
                            skipped += 1
                            continue
                        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
                            skipped += 1
                            continue
                        guru = User(username=username, email=email, phone_number=phone_number, is_guru=True)
                        guru.set_password(password)
                        guru.save()
                        added += 1
                    messages.success(request, f'Import selesai: {added} guru ditambahkan, {skipped} baris dilewati.')
                    return redirect('admin_guru_list')
                except Exception as exc:
                    messages.error(request, str(exc))
        else:
            form = GuruRegistrationForm(request.POST)
            if form.is_valid():
                guru = form.save(commit=False)
                guru.set_password(form.cleaned_data['password'])
                guru.is_guru = True
                guru.save()
                messages.success(request, 'Data Guru berhasil ditambahkan.')
                return redirect('admin_guru_list')

    gurus = User.objects.filter(is_guru=True)
    return render(request, 'dashboards/admin/guru.html', {'gurus': gurus, 'form': form, 'import_form': import_form})


@login_required
def admin_santri_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    form = StudentForm()
    import_form = ImportStudentForm()

    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            santri_id = request.POST.get('santri_id')
            try:
                santri = Student.objects.get(id=santri_id)
                santri.delete()
                messages.success(request, 'Data Santri berhasil dihapus.')
            except Student.DoesNotExist:
                messages.error(request, 'Data Santri tidak ditemukan.')
            return redirect('admin_santri_list')
        elif request.POST.get('submit_type') == 'import_santri':
            import_form = ImportStudentForm(request.POST, request.FILES)
            if import_form.is_valid():
                try:
                    from datetime import datetime
                    rows = parse_import_file(import_form.cleaned_data['xlsx_file'])
                    added = 0
                    skipped = 0
                    for row in rows:
                        # Extract field dengan berbagai alias
                        nis = (row.get('nis') or row.get('NIS') or '').strip()
                        name = (row.get('name') or row.get('Name') or '').strip()
                        grade = (row.get('grade') or row.get('Grade') or '').strip()
                        birth_date_str = (row.get('birth_date') or row.get('Birth Date') or '').strip()
                        parent_key = (row.get('parent_username') or row.get('Parent Username') or row.get('parent_email') or row.get('Parent Email') or '').strip()
                        
                        # Validasi field yang wajib
                        if not nis or not name or not grade or not birth_date_str:
                            skipped += 1
                            continue
                        
                        # Parse tanggal dengan berbagai format
                        birth_date = None
                        for date_format in ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y', '%m/%d/%Y']:
                            try:
                                birth_date = datetime.strptime(birth_date_str, date_format).date()
                                break
                            except ValueError:
                                continue
                        
                        if not birth_date:
                            skipped += 1
                            continue
                        
                        # Parent bersifat opsional
                        parent = None
                        if parent_key:
                            parent = User.objects.filter(is_parent=True).filter(Q(username=parent_key) | Q(email=parent_key)).first()
                        
                        # Validasi NIS unik
                        if Student.objects.filter(nis=nis).exists():
                            skipped += 1
                            continue
                        
                        Student.objects.create(parent=parent, nis=nis, name=name, grade=grade, birth_date=birth_date)
                        added += 1
                    messages.success(request, f'Import selesai: {added} santri ditambahkan, {skipped} baris dilewati.')
                    return redirect('admin_santri_list')
                except Exception as exc:
                    messages.error(request, f'Error saat import: {str(exc)}')
        else:
            form = StudentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Data Santri berhasil ditambahkan.')
                return redirect('admin_santri_list')

    santris = Student.objects.all().select_related('parent')
    return render(request, 'dashboards/admin/santri.html', {'santris': santris, 'form': form, 'import_form': import_form})


@login_required
def admin_finance_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    payment_form = PaymentForm()
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        action = request.POST.get('action')
        if action in ['approve', 'reject', 'delete'] and payment_id:
            try:
                payment = Payment.objects.get(id=payment_id)
                if action == 'approve':
                    payment.status = 'lunas'
                    messages.success(request, f'Status pembayaran {payment.student.name} berhasil diubah menjadi lunas.')
                elif action == 'reject':
                    payment.status = 'ditolak'
                    messages.success(request, f'Status pembayaran {payment.student.name} berhasil ditolak.')
                elif action == 'delete':
                    student_name = payment.student.name
                    payment.delete()
                    messages.success(request, f'Tagihan SPP untuk {student_name} berhasil dihapus.')
                    return redirect('admin_finance_list')
                payment.save()
            except Payment.DoesNotExist:
                messages.error(request, 'Data pembayaran tidak ditemukan.')
            return redirect('admin_finance_list')

        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            payment_form.save()
            messages.success(request, 'Tagihan SPP berhasil dibuat.')
            return redirect('admin_finance_list')

    payments = Payment.objects.all().select_related('student').order_by('-created_at')
    return render(request, 'dashboards/admin/finance.html', {'payments': payments, 'payment_form': payment_form})

@login_required
def admin_permit_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST':
        permit_id = request.POST.get('permit_id')
        action = request.POST.get('action')
        if action in ['approve', 'reject', 'delete'] and permit_id:
            try:
                permit = Permit.objects.get(id=permit_id)
                if action == 'approve':
                    permit.status = 'disetujui'
                    messages.success(request, f'Status perizinan {permit.student.name} berhasil disetujui.')
                elif action == 'reject':
                    permit.status = 'ditolak'
                    messages.success(request, f'Status perizinan {permit.student.name} berhasil ditolak.')
                elif action == 'delete':
                    student_name = permit.student.name
                    permit.delete()
                    messages.success(request, f'Permintaan izin {student_name} berhasil dihapus.')
                    return redirect('admin_permit_list')
                permit.save()
            except Permit.DoesNotExist:
                messages.error(request, 'Data izin tidak ditemukan.')
            return redirect('admin_permit_list')

    permits = Permit.objects.all().select_related('student').order_by('-created_at')
    return render(request, 'dashboards/admin/permit.html', {'permits': permits})

@login_required
def admin_behavior_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST' and 'delete_behavior_id' in request.POST:
        behavior_id = request.POST.get('delete_behavior_id')
        try:
            behavior = BehaviorNote.objects.get(id=behavior_id)
            behavior.delete()
            messages.success(request, 'Catatan perilaku berhasil dihapus.')
        except BehaviorNote.DoesNotExist:
            messages.error(request, 'Catatan perilaku tidak ditemukan.')
        return redirect('admin_behavior_list')

    if request.method == 'POST':
        form = BehaviorNoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catatan sikap berhasil ditambahkan.')
            return redirect('admin_behavior_list')
    else:
        form = BehaviorNoteForm()

    behaviors = BehaviorNote.objects.all().select_related('student').order_by('-date', '-id')
    return render(request, 'dashboards/admin/behavior.html', {'behaviors': behaviors, 'form': form})

@login_required
def edit_finance(request, payment_id):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tagihan SPP berhasil diubah.')
            return redirect('admin_finance_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'dashboards/admin/edit_finance.html', {'form': form, 'payment': payment})

@login_required
def edit_permit(request, permit_id):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    permit = get_object_or_404(Permit, id=permit_id)
    if request.method == 'POST':
        form = PermitForm(request.POST, instance=permit)
        if form.is_valid():
            form.save()
            messages.success(request, 'Permintaan izin berhasil diubah.')
            return redirect('admin_permit_list')
    else:
        form = PermitForm(instance=permit)
    return render(request, 'dashboards/admin/edit_permit.html', {'form': form, 'permit': permit})

@login_required
def edit_behavior(request, behavior_id):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    behavior = get_object_or_404(BehaviorNote, id=behavior_id)
    if request.method == 'POST':
        form = BehaviorNoteForm(request.POST, instance=behavior)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catatan perilaku berhasil diubah.')
            return redirect('admin_behavior_list')
    else:
        form = BehaviorNoteForm(instance=behavior)
    return render(request, 'dashboards/admin/edit_behavior.html', {'form': form, 'behavior': behavior})


@login_required
def admin_parent_list(request):
    """Admin page untuk mengelola data wali murid."""
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST':
        if request.POST.get('action') == 'delete':
            parent_id = request.POST.get('parent_id')
            try:
                parent = User.objects.get(id=parent_id, is_parent=True)
                parent.delete()
                messages.success(request, 'Data Wali Murid berhasil dihapus.')
            except User.DoesNotExist:
                messages.error(request, 'Data Wali Murid tidak ditemukan.')
            return redirect('admin_parent_list')

    parents = User.objects.filter(is_parent=True).prefetch_related('children')
    return render(request, 'dashboards/admin/parent.html', {'parents': parents})


@login_required
def edit_parent(request, parent_id):
    """Edit data wali murid."""
    parent = get_object_or_404(User, id=parent_id, is_parent=True)
    
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST':
        parent.username = request.POST.get('username', parent.username)
        parent.email = request.POST.get('email', parent.email)
        parent.phone_number = request.POST.get('phone_number', parent.phone_number)
        # Jika admin memasukkan password baru, set password
        new_password = request.POST.get('password')
        if new_password:
            parent.set_password(new_password)
        parent.save()
        messages.success(request, 'Data Wali Murid berhasil diubah.')
        return redirect('admin_parent_list')

    return render(request, 'dashboards/admin/edit_parent.html', {'parent': parent})


@login_required
def edit_santri(request, santri_id):
    """Edit data santri."""
    santri = get_object_or_404(Student, id=santri_id)
    
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=santri)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Santri berhasil diubah.')
            return redirect('admin_santri_list')
    else:
        form = StudentForm(instance=santri)

    return render(request, 'dashboards/admin/edit_santri.html', {'form': form, 'santri': santri})


@login_required
def edit_guru(request, guru_id):
    """Edit data guru."""
    guru = get_object_or_404(User, id=guru_id, is_guru=True)
    
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')

    if request.method == 'POST':
        guru.username = request.POST.get('username', guru.username)
        guru.email = request.POST.get('email', guru.email)
        guru.phone_number = request.POST.get('phone_number', guru.phone_number)
        # Jika admin memasukkan password baru, set password
        new_password = request.POST.get('password')
        if new_password:
            guru.set_password(new_password)
        guru.save()
        messages.success(request, 'Data Guru berhasil diubah.')
        return redirect('admin_guru_list')

    return render(request, 'dashboards/admin/edit_guru.html', {'guru': guru})


@login_required
def upload_profile_picture(request):
    """View untuk menangani unggahan foto profil mandiri dari pengguna."""
    if request.method == 'POST' and request.FILES.get('profile_picture'):
        request.user.profile_picture = request.FILES['profile_picture']
        request.user.save()
        messages.success(request, 'Foto profil Anda berhasil diperbarui.')
    else:
        messages.error(request, 'Gagal memperbarui foto profil. File tidak valid.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
def mark_notification_read(request, notification_id):
    """View untuk menandai satu notifikasi sebagai telah dibaca."""
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@login_required
def mark_all_notifications_read(request):
    """View untuk menandai semua notifikasi pengguna sebagai telah dibaca."""
    request.user.notifications.filter(is_read=False).update(is_read=True)
    return JsonResponse({'status': 'success'})

