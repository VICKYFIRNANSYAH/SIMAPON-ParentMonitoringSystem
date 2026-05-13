from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register_parent, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/guru/', views.guru_dashboard, name='guru_dashboard'),
    path('dashboard/parent/', views.parent_dashboard, name='parent_dashboard'),
    path('dashboard/admin/guru/', views.admin_guru_list, name='admin_guru_list'),
    path('dashboard/admin/santri/', views.admin_santri_list, name='admin_santri_list'),
    path('dashboard/admin/finance/', views.admin_finance_list, name='admin_finance_list'),
    path('dashboard/admin/permit/', views.admin_permit_list, name='admin_permit_list'),
    path('dashboard/admin/behavior/', views.admin_behavior_list, name='admin_behavior_list'),
]
