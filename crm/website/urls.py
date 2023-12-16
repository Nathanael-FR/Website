from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('user_login/', views.user_login, name="user_login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('login_patient/', views.login_patient, name="login_patient"),
    path('booking', views.booking, name = "booking"),
    path('get_doctors/', views.get_doctors, name='get_doctors'),
    path('get_availabilities/', views.get_availabilities, name='get_availabilities'),
    path('confirm_appointment/', views.confirm_appointment, name='confirm_appointment'),
    path('profil', views.profil, name="profil"),
    path('dashboard/doc_dash', views.doc_dashboard, name="doc_dashboard"),
    path('dashboard/pat_dash', views.pat_dashboard, name="pat_dashboard"),
    path('dashboard/app_dash', views.app_dashboard, name="app_dashboard"),
    path('profil/appointment', views.show_patient_appointment, name='patient_appointments'),
    path('profil/edit_profil', views.edit_patient_profil, name='edit_profil'),
    path('contacts', views.contacts, name='contacts'),



]
