from django.shortcuts import render
from .models import Student, Attendance
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime

def student_dashboard(request):
    students = Student.objects.all().order_by('seat_number')
    
    # Analytics Calculation
    total_students = students.count()
    total_revenue = students.filter(is_fees_paid=True).aggregate(Sum('monthly_fees'))['monthly_fees__sum'] or 0
    total_pending = students.filter(is_fees_paid=False).aggregate(Sum('monthly_fees'))['monthly_fees__sum'] or 0
    defaulters_count = students.filter(is_fees_paid=False).count()

    # SAHI VALI FIELD: Aaj jin bacho ka check-in ho chuka hai unki IDs (is_present=True)
    today = datetime.date.today()
    checked_in_today = Attendance.objects.filter(date=today, is_present=True).values_list('student_id', flat=True)

    # Visual Seat Map Logic (30 Seats)
    seat_map = []
    booked_seats = {s.seat_number: s for s in students}
    
    for seat_no in range(1, 31):
        if seat_no in booked_seats:
            seat_map.append({
                'number': seat_no,
                'is_booked': True,
                'student': booked_seats[seat_no]
            })
        else:
            seat_map.append({
                'number': seat_no,
                'is_booked': False,
                'student': None
            })

    context = {
        'students': students,
        'total_students': total_students,
        'total_revenue': total_revenue,
        'total_pending': total_pending,
        'defaulters_count': defaulters_count,
        'seat_map': seat_map,
        'checked_in_today': checked_in_today,
    }
    return render(request, 'books/book_list.html', context)

# NAYA VIEW: Attendance toggle karne ka exact database control
@csrf_exempt
def mark_attendance(request, student_id):
    if request.method == 'POST':
        try:
            student = Student.objects.get(id=student_id)
            today = datetime.date.today()
            
            existing_attendance = Attendance.objects.filter(student=student, date=today)
            if existing_attendance.exists():
                existing_attendance.delete()
                return JsonResponse({'status': 'unmarked'})
            else:
                # Yahan bhi is_present=True use kiya
                Attendance.objects.create(student=student, date=today, is_present=True)
                return JsonResponse({'status': 'marked'})
                
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
    return JsonResponse({'error': 'Invalid request'}, status=400)