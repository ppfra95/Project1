from django.urls import path

from . import views

app_name = 'UserAuth'

urlpatterns = [
    # path('login/', views.CustomAuthToken.as_view()),
    # path('users/', views.ListUsers.as_view()),
    # path('user/<pk>/edit/', views.EditUser.as_view()),
    # path('user/<pk>/change-password/', views.UserChangePassword.as_view()),
    # path('create/', views.CreateUser.as_view()),
    path('login/', views.CreateTokenView.as_view()),
    path('user/', views.ManageUserView.as_view()),
    path('create/', views.CreateUserView.as_view()),
]
