from django.urls import path
from . import views
from .views import login_view  # Import the login view

from django.contrib.auth import views as auth_views

#URLConfig
urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('packages/', views.packages_view, name='packages'),
    
    path('modules/<int:package_id>/', views.modules_view, name='modules'),

    path('quizzes/<int:module_id>/', views.quizzes_view, name='quizzes'),

    path('questions/<int:quiz_id>/', views.questions_view, name='questions'),
   
    path('result/', views.results_view, name='result'),


    path('quiz/<int:quiz_id>/', views.quiz_detail_view, name='quiz_detail'),  # URL for quiz details
    
    path('quiz_detail/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    
    path('quiz/<int:quiz_id>/take/', views.take_quiz, name='take_quiz'),  # ensure this matches

    # path('quizzes/', views.take_quiz, name='take_quiz'),  # ensure this matches


    path('buyPackages/<int:package_id>/', views.buyPackages, name='buyPackages'),
    
    

    path('packages/<int:package_id>/', views.packages_view, name='package_view'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/quizzes/'), name='logout'),
    #for passwords reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='quizzes/password_reset_form.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]

