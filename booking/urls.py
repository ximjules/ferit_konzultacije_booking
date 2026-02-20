from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.SlotListView.as_view(), name="slot_list"),
    path("slots/<int:pk>/", views.SlotDetailView.as_view(), name="slot_detail"),
    path("slots/<int:slot_pk>/book/", views.book_slot, name="book_slot"),
    path("my-bookings/", views.MyBookingsView.as_view(), name="my_bookings"),
]
