from django.urls import path

from .views import  LoginView, LogoutView, UserView, aPage, registerView





urlpatterns = [
    path('a/', aPage),
    path('register/', registerView),
    path('login/', LoginView),
    path('user/', UserView),
    path('Logout/', LogoutView),
   
]