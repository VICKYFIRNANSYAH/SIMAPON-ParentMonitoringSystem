import os
from abc import ABC, abstractmethod
from users.models import User
from students.models import Student
from finance.models import Payment
from permits.models import Permit
from behavior.models import BehaviorNote

class DashboardReport(ABC):
    def __init__(self, user):
        self._user = user  

    @abstractmethod
    def get_summary(self):
        pass

    @property
    def user(self):
        return self._user


class AdminDashboardReport(DashboardReport):
    def get_summary(self):
        return {
            'total_guru': self.__count_gurus(), 
            'total_santri': self.__count_students(),
            'total_spp_pending': self.__count_pending_payments(),
            'total_izin_pending': self.__count_pending_permits(),
        }

    def __count_gurus(self):
        return User.objects.filter(is_guru=True).count()

    def __count_students(self):
        return Student.objects.count()

    def __count_pending_payments(self):
        return Payment.objects.filter(status='menunggu').count()

    def __count_pending_permits(self):
        return Permit.objects.filter(status='menunggu').count()


class GuruDashboardReport(DashboardReport):
    def get_summary(self):
        return {
            'students_count': self.__count_students(),
            'pending_permits_count': self.__count_pending_permits(),
            'notes_count': self.__count_behavior_notes(),
        }

    def __count_students(self):
        return Student.objects.count()

    def __count_pending_permits(self):
        return Permit.objects.filter(status='menunggu').count()

    def __count_behavior_notes(self):
        return BehaviorNote.objects.count()


class ParentDashboardReport(DashboardReport):
    def get_summary(self):
        children = self._user.children.all()
        payments = Payment.objects.filter(student__parent=self._user).select_related('student').order_by('-created_at')
        
        return {
            'children': children,
            'payments': payments,
            'children_count': children.count(),
            'pending_payments_count': payments.exclude(status='lunas').count(),
            'behavior_notes': BehaviorNote.objects.filter(student__parent=self._user).select_related('student').order_by('-date', '-id'),
            'permits': Permit.objects.filter(student__parent=self._user).select_related('student').order_by('-created_at'),
        }
