from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'department', 'branch', 'date', 'first_punch', 'last_punch', 'total_time')
    list_filter = ('department', 'branch', 'date')
    search_fields = ('employee_id', 'first_name', 'department', 'branch')
