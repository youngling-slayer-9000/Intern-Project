from django.db import models

class AttendanceRecord(models.Model):
    employee_id = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, default="")  # 🆕 New field
    date = models.DateField()
    first_punch = models.TimeField()
    last_punch = models.TimeField()
    total_time = models.DurationField()

    def __str__(self):
        return f"{self.date} - {self.employee_id} ({self.first_name}) - {self.first_punch} to {self.last_punch} ({self.total_time})"
