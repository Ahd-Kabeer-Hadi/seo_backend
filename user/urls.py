from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('details/', views.UserDetails.as_view(), name='user-details'),
]
