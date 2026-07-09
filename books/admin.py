from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('seat_number', 'name', 'mobile', 'shift_plan', 'is_fees_paid')
    list_filter = ('shift_plan', 'is_fees_paid')
    search_fields = ('name', 'mobile', 'seat_number')

admin.site.register(Attendance)