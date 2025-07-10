from django.contrib import admin


from .models import EmployeeUser

from django.contrib import admin
from .models import EmployeeUser
from django.contrib.auth.hashers import make_password

@admin.register(EmployeeUser)
class EmployeeUserAdmin(admin.ModelAdmin):
    list_display = ['username']
    fields = ['username', 'password']

    def save_model(self, request, obj, form, change):
        # Hash the password if it's being created or changed
        if not change or 'password' in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)
