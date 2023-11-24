from django.apps import apps
from django.contrib import admin
from unfold.admin import ModelAdmin
# Register your models here.
from .models import Kwiat, Kolory, Raport, Zamowienie
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django_celery_results.models import TaskResult, GroupResult
from django.contrib.auth.models import User

# Unregister TaskResult and GroupResult from admin
try:
    admin.site.unregister(TaskResult)
except admin.sites.NotRegistered:
    pass

try:
    admin.site.unregister(GroupResult)
except admin.sites.NotRegistered:
    pass
    
# @admin.register(User)
# class UserAdmin(BaseUserAdmin, ModelAdmin):
#     pass
    
    
@admin.register(Kolory)
class KoloryAdmin(ModelAdmin):
    list_display = (
        "name",
        "hex_kolor",
    )
    
@admin.register(Raport)
class RaportAdmin(ModelAdmin):
    list_display = (
        "id",
        "data_utworzenia",
    )        
    
@admin.register(Kwiat)
class KwiatAdmin(ModelAdmin):
    list_display = (
        "name",
        "aktywny",
        "kolejnosc",
    )    
    
@admin.register(Zamowienie)
class ZamowienieAdmin(ModelAdmin):
    list_display = (
        "id",
        "odbiorca",
        "termin_dostarczenia",
    )    