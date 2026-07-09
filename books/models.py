from django.db import models
from django.utils import timezone

# 1. Students ka poora data (Membership Tracking)
class Student(models.Model):
    PLAN_CHOICES = [
        ('6_HOURS', '6 Hours Shift'),
        ('12_HOURS', '12 Hours Shift'),
        ('FULL_DAY', '24 Hours Full Day'),
    ]
    
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    joined_date = models.DateField(default=timezone.now)
    seat_number = models.IntegerField(unique=True) # Har bache ki apni fixed seat
    shift_plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='12_HOURS')
    monthly_fees = models.IntegerField(default=1000) # Kitni fees h
    is_fees_paid = models.BooleanField(default=True) # Fees status

    def __str__(self):
        return f"Seat {self.seat_number} - {self.name}"

# 2. Daily Attendance Board (Kaun bacha aaj aaya)
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.name} - {self.date} - {'Present' if self.is_present else 'Absent'}"