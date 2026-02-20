from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("", views.home, name="home"),
    path("slots/<int:slot_pk>/book/", views.book_slot, name="book_slot"),
    path("my-bookings/", views.MyBookingsView.as_view(), name="my_bookings"),
    path("my-bookings/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),

    path("mentor/slots/", views.mentor_slots, name="mentor_slots"),
    path("mentor/slots/add/", views.mentor_add_slot, name="mentor_add_slot"),

    path("slots/", views.SlotListView.as_view(), name="slot_list"),
    path("slots/<int:pk>/", views.SlotDetailView.as_view(), name="slot_detail"),
]
