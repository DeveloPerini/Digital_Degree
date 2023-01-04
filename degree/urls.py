from django.urls import path , include
from . import views

urlpatterns = [
    path('' , views.home),
    path('signin/', views.SignIn , name= 'signin'),
    path('login/', views.Login , name= 'login'),
    path('add_student/', views.add_student , name='add_student'),
    path('student_list/', views.student_list , name= 'student_list'),
    path('search/', views.search , name= 'search'),
    path('student_details/', views.student_details , name= 'student_details'),
    path('logout/', views.logout_view, name='logout'),
]

