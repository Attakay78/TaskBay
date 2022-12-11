from django.urls import path 

from authentication_app import views

urlpatterns = [
    path('signup/', views.AuthenticateUser.as_view()),
    path('signin/', views.AuthenticateUser.as_view()),
    path('updateuser/<str:email>/', views.AuthenticateUser.as_view()),
    path('deleteuser/<str:email>/', views.AuthenticateUser.as_view())
]
