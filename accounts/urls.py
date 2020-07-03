"""CMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views 
from . import views

urlpatterns = [
    
    # path('test/', views.test, name='test'),
    path('user/list/', views.user_list, name='user-list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('admission/hsc/', views.signup_hsc, name='signup'),
    path('admission/honours/', views.signup_honours, name='signup-h'),   
    path('admission/ibm/', views.signup_ibm, name='signup-ibm'),   
    path('admission/degree/', views.signup_degree, name='signup-degree'),   
    path('dashboard/', views.admin_dashboard, name='admin'),
    path('add/principal/', views.add_principal, name='add-principal'),
    path('dashboard/add/teacher/', views.add_teacher, name='add-teacher'),
    path('add/staff/', views.add_staff, name='add-staff'),
    path('dashboard/profile/<str:id>/', views.profile, name='show-profile'),
    path('download/<str:username>/', views.download_form, name='download'),
    # path('dashboard/teacher/appoint/<str:id>/', views.wil_take, name='will-take'),
    path('dashboard/list/teacher/<str:dept_name>/', views.teachersList, name='show-teachers-list'),
    path('add/notice/', views.notice, name='add-notice'),
    path('add/photo/', views.photo, name='add-photo'),
    path('add/books/', views.books, name='add-books'),
    path('add/depertment/', views.depertment, name='add-depertment'),
    path('add/subject/', views.subject, name='add-subject'),
    path('add/session/', views.session, name='session'),
    path('add/roll/hsc/science/', views.roll_hsc_science, name='roll-hsc-science'),
    path('add/roll/hsc/business-studies/', views.roll_hsc_commarts, name='roll-hsc-commarts'),
    path('add/roll/hsc/humanities/a/', views.roll_hsc_arts_a, name='roll-hsc-Humanities(A)'),
    path('add/roll/hsc/humanities/b/', views.roll_hsc_arts_b, name='roll-hsc-Humanities(B)'),
    path('add/roll/honours/bangla/', views.roll_honours_bangla, name='roll-honours-bangla'),
    path('add/roll/honours/accounting/', views.roll_honours_accounting, name='roll-honours-accounting'),
    path('add/roll/honours/geography/', views.roll_honours_geography, name='roll-honours-geography'),
    path('add/roll/honours/management/', views.roll_honours_management, name='roll-honours-management'),
    path('add/roll/degree/bba/', views.roll_degree_bba, name='roll-degree-bba'),
    path('add/roll/degree/ba/', views.roll_degree_ba, name='roll-degree-ba'),
    path('add/roll/degree/bss/', views.roll_degree_bss, name='roll-degree-bss'),
    path('add/roll/ibm/', views.roll_ibm, name='roll-ibm'),
    path('add/roll/', views.add_roll, name='add-roll'),
    path('add/session/save/', views.session_save, name='save_session'),
    path('add/session/show/', views.session_show, name='show_session'),
    path('add/year/', views.year, name='year'),
    path('payment/', views.monthly_payment, name='monthly-payment'),
    path('payment/donation/', views.donation, name='donation'),
    path('payment/<str:id>/', views.payment, name='payment'),
    path('pardon/<str:id>/', views.pardon , name='pardon'),
    path('expense/', views.expense , name='expense'),
    
    # path('add/notice/', views.notice, name='add-staff'),

    path('activate/<uidb64>/<token>/',views.activate, name='activate'),
    
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    
]


