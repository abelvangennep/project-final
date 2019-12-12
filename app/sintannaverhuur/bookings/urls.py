from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("book", views.book, name="book"),
    path("indeling", views.indeling, name="indeling"),
    path("getbooking", views.get_booking, name="get_booking"),
    path("contact", views.contact, name="contact")
]


