from django.urls import path
from tickets import views

urlpatterns = [
    path('tickets/', views.TicketList.as_view(), name='ticket_list'),
    path('tickets/<int:pk>/', views.TicketDetail.as_view(), name='ticket_detail'),  # Noqa E501
]
