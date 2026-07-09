from django.contrib import admin
from django.urls import path
from books import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.student_dashboard, name='student_dashboard'),
    path('attendance/<int:student_id>/', views.mark_attendance, name='mark_attendance'), # Yeh line add ki
]