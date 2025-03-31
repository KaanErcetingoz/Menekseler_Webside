from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('documents/', views.documents, name='documents'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('translate-text/', views.translate_text, name='translate_text'),
    path('contact/', views.contact, name='contact'),
    path('diet-program/', views.diet_program, name='diet_program'),
]
