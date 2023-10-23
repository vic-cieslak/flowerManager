from django.urls import path

from . import views

urlpatterns = [
    path("", views.datatables, name="datatables"),
    path("kolory", views.kolory, name="kolory"),
    path("kolejnosc", views.kolejnosc, name="kolejnosc"),
    path("raport_start", views.raport_start, name="raport_start"),
    path("lista_raportow", views.lista_raportow, name="lista_raportow"),
    path("delete-kolor/<int:id>/", views.delete_kolor, name="delete_kolor"),
    path("zmien_status/<int:id>/", views.zmien_status, name="zmien_status"),
    path('update-kolor/<int:id>/', views.update_kolor, name="update_kolor"),
    path('delete-kwiat/<int:id>/', views.delete_kwiat, name="delete_kwiat"),
    path('edytuj-kwiat/<int:id>/', views.edytuj_kwiat, name="edytuj_kwiat"),
    path('update-product/<int:id>/', views.update_product, name="update_product"),
]