from django.urls import path
from authentication import views

urlpatterns = [
    path('register/', views.RegisterUser.as_view(), name='register'),
]
