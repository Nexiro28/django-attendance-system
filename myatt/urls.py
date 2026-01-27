from django.urls import path
from . import views

urlpatterns = [
    # pages
    path('', views.login_view),
    path('register/', views.register_view),
    path('attendance/', views.attendance_view),

    # APIs
    path('api/subjects/', views.get_subjects),
    path('api/add/', views.add_subject),
    path('api/mark/', views.mark_attendance),
    path('api/delete/', views.delete_subject),
]
