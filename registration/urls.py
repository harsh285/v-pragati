from django.urls import path
from registration import views
from django.contrib.auth import views as auth_views

app_name = 'registration'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signUp'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='registration:login'), name='logout'),
]
