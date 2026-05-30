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
    path('dashboard/admin/parent/', views.admin_parent_list, name='admin_parent_list'),
    path('dashboard/admin/finance/', views.admin_finance_list, name='admin_finance_list'),
    path('dashboard/admin/finance/edit/<int:payment_id>/', views.edit_finance, name='edit_finance'),
    path('dashboard/admin/permit/', views.admin_permit_list, name='admin_permit_list'),
    path('dashboard/admin/permit/edit/<int:permit_id>/', views.edit_permit, name='edit_permit'),
    path('dashboard/admin/behavior/', views.admin_behavior_list, name='admin_behavior_list'),
    path('dashboard/admin/behavior/edit/<int:behavior_id>/', views.edit_behavior, name='edit_behavior'),
    path('dashboard/admin/edit-parent/<int:parent_id>/', views.edit_parent, name='edit_parent'),
    path('dashboard/admin/edit-santri/<int:santri_id>/', views.edit_santri, name='edit_santri'),
    path('dashboard/admin/edit-guru/<int:guru_id>/', views.edit_guru, name='edit_guru'),
    path('dashboard/profile/upload/', views.upload_profile_picture, name='upload_profile_picture'),
    path('notifications/mark-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]

