from django.urls import path

from . import views

urlpatterns = [
    path("", views.datatables, name="datatables"),
    path("kolory", views.kolory, name="kolory"),
    path("delete-kolor/<int:id>/", views.delete_kolor, name="delete_kolor"),
    path('update-kolor/<int:id>/', views.update_kolor, name="update_kolor"),
    path('delete-product/<int:id>/', views.delete_product, name="delete_product"),
    path('update-product/<int:id>/', views.update_product, name="update_product"),
]