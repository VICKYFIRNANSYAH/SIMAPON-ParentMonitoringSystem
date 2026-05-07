from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ParentRegistrationForm
from students.models import Student

def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
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
    return render(request, 'dashboards/admin.html')

@login_required
def guru_dashboard(request):
    return render(request, 'dashboards/guru.html')

@login_required
def parent_dashboard(request):
    children = request.user.children.all()
    return render(request, 'dashboards/parent.html', {'children': children})
