from django.urls import path

from . import views

urlpatterns = [
    path("", views.datatables, name="datatables"),
    path("kolory", views.kolory, name="kolory"),
    path("kolejnosc", views.kolejnosc, name="kolejnosc"),
    path("raport_start", views.raport_start, name="raport_start"),
    path("lista_raportow", views.lista_raportow, name="lista_raportow"),
    path("dodaj_zamowienie", views.dodaj_zamowienie, name="dodaj_zamowienie"),
    path("archiwum_zamowien", views.archiwum_zamowien, name="archiwum_zamowien"),
    path("lista_zamowien", views.lista_zamowien, name="lista_zamowien"),
    path("usun_raport/<int:id>/", views.usun_raport, name="usun_raport"),
    path("usun_zamowienie/<int:id>/", views.usun_zamowienie, name="usun_zamowienie"),
    path("zmien_status_zamowienia/<int:id>/", views.zmien_status_zamowienia, name="zmien_status_zamowienia"),
    path("przenies_do_archiwum/<int:id>/", views.przenies_do_archiwum, name="przenies_do_archiwum"),
    path("delete-kolor/<int:id>/", views.delete_kolor, name="delete_kolor"),
    path("czytaj_raport/<int:id>/", views.czytaj_raport, name="czytaj_raport"),
    path("czytaj_raport/<int:id>/kupic", views.czytaj_raport_do_kupienia, name="czytaj_raport_do_kupienia"),
    path("zmien_status/<int:id>/", views.zmien_status, name="zmien_status"),
    path('update-kolor/<int:id>/', views.update_kolor, name="update_kolor"),
    path('delete-kwiat/<int:id>/', views.delete_kwiat, name="delete_kwiat"),
    path('edytuj-kwiat/<int:id>/', views.edytuj_kwiat, name="edytuj_kwiat"),
    path('edytuj-zamowienie/<int:id>/', views.edytuj_zamowienie, name="edytuj_zamowienie"),
    path('odswiez-kolory/<int:id>/', views.odswiez_kolory, name="odswiez_kolory"),
    path('update-product/<int:id>/', views.update_product, name="update_product"),
]