from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    # Home (lista dostupnih termina)
    path("", views.home, name="home"),

    # Student - rezervacija
    path("slots/<int:slot_pk>/book/", views.book_slot, name="book_slot"),

    # Student - moje rezervacije
    path("my-bookings/", views.MyBookingsView.as_view(), name="my_bookings"),

    # Mentor - upravljanje terminima
    path("mentor/slots/", views.mentor_slots, name="mentor_slots"),
    path("mentor/slots/add/", views.mentor_add_slot, name="mentor_add_slot"),

    # (Opcionalno) klasični list/detail viewovi ako ih želiš koristiti kasnije
    path("slots/", views.SlotListView.as_view(), name="slot_list"),
    path("slots/<int:pk>/", views.SlotDetailView.as_view(), name="slot_detail"),
]
