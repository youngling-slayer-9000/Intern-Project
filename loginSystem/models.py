from django.db import models

class EmployeeUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return self.username
