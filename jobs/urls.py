from django.urls import path
from . import views

urlpatterns = [
    path('', views.operative_form, name='operative_form'),
    path('success/<int:job_id>/', views.job_success, name='job_success'),
    path('dashboard/', views.qs_dashboard, name='qs_dashboard'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]
