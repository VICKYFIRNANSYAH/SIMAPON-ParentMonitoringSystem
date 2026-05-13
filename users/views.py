from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ParentRegistrationForm, GuruRegistrationForm
from django.contrib import messages
from students.models import Student
from users.models import User
from finance.models import Payment
from permits.models import Permit

def landing_page(request):
    return render(request, 'landing.html')

def register_parent(request):
    if request.method == 'POST':
        form = ParentRegistrationForm(request.POST)
        if form.is_valid():
            # Create User
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_parent = True
            user.save()
            
            # Create Student
            Student.objects.create(
                parent=user,
                nis=form.cleaned_data['student_nis'],
                name=form.cleaned_data['student_name'],
                grade=form.cleaned_data['student_grade'],
                birth_date=form.cleaned_data['student_birth_date']
            )
            
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

# Temporary placeholders for the dashboards
@login_required
def admin_dashboard(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
    
    context = {
        'total_guru': User.objects.filter(is_guru=True).count(),
        'total_santri': Student.objects.count(),
        'total_spp_pending': Payment.objects.filter(status='menunggu').count(),
        'total_izin_pending': Permit.objects.filter(status='menunggu').count(),
    }
    return render(request, 'dashboards/admin.html', context)

@login_required
def guru_dashboard(request):
    return render(request, 'dashboards/guru.html')

@login_required
def parent_dashboard(request):
    children = request.user.children.all()
    return render(request, 'dashboards/parent.html', {'children': children})

@login_required
def admin_guru_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = GuruRegistrationForm(request.POST)
        if form.is_valid():
            guru = form.save(commit=False)
            guru.set_password(form.cleaned_data['password'])
            guru.is_guru = True
            guru.save()
            messages.success(request, 'Data Guru berhasil ditambahkan.')
            return redirect('admin_guru_list')
    else:
        form = GuruRegistrationForm()
        
    gurus = User.objects.filter(is_guru=True)
    return render(request, 'dashboards/admin_guru.html', {'gurus': gurus, 'form': form})

from students.forms import StudentForm

@login_required
def admin_santri_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Data Santri berhasil ditambahkan.')
            return redirect('admin_santri_list')
    else:
        form = StudentForm()
        
    santris = Student.objects.all().select_related('parent')
    return render(request, 'dashboards/admin_santri.html', {'santris': santris, 'form': form})

@login_required
def admin_finance_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
        
    if request.method == 'POST' and 'action' in request.POST:
        payment_id = request.POST.get('payment_id')
        action = request.POST.get('action')
        try:
            payment = Payment.objects.get(id=payment_id)
            if action == 'approve':
                payment.status = 'lunas'
            elif action == 'reject':
                payment.status = 'ditolak'
            payment.save()
            messages.success(request, f'Status pembayaran {payment.student.name} berhasil diubah.')
        except Payment.DoesNotExist:
            pass
        return redirect('admin_finance_list')
        
    payments = Payment.objects.all().select_related('student').order_by('-created_at')
    return render(request, 'dashboards/admin_finance.html', {'payments': payments})

@login_required
def admin_permit_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
        
    if request.method == 'POST' and 'action' in request.POST:
        permit_id = request.POST.get('permit_id')
        action = request.POST.get('action')
        try:
            permit = Permit.objects.get(id=permit_id)
            if action == 'approve':
                permit.status = 'disetujui'
            elif action == 'reject':
                permit.status = 'ditolak'
            permit.save()
            messages.success(request, f'Status perizinan {permit.student.name} berhasil diubah.')
        except Permit.DoesNotExist:
            pass
        return redirect('admin_permit_list')
        
    permits = Permit.objects.all().select_related('student').order_by('-created_at')
    return render(request, 'dashboards/admin_permit.html', {'permits': permits})

from behavior.forms import BehaviorNoteForm
from behavior.models import BehaviorNote

@login_required
def admin_behavior_list(request):
    if not (request.user.is_admin or request.user.is_staff):
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = BehaviorNoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Catatan sikap berhasil ditambahkan.')
            return redirect('admin_behavior_list')
    else:
        form = BehaviorNoteForm()
        
    behaviors = BehaviorNote.objects.all().select_related('student').order_by('-date', '-id')
    return render(request, 'dashboards/admin_behavior.html', {'behaviors': behaviors, 'form': form})
