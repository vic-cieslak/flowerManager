from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from apps.tables.forms import ProductForm, KoloryForm
from apps.common.models import Product, Kolory, Kwiat, Raport
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.tables.utils import product_filter
import json
from django.contrib import messages
from django.db.models.functions import Lower

# Create your views here.
# @login_required(login_url='/users/signin/')
def datatables(request):
  filters = product_filter(request)
  kwiaty_list = Kwiat.objects.filter(**filters).order_by(Lower('name'))
  kolory = Kolory.objects.all()
  
  
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
      
  for kwiat in kwiaty_list:
    kwiat.kategorie_i_kolory_list = json.loads(json.loads(kwiat.kategorie_i_kolory))


  page = request.GET.get('page', 1)
#   paginator = Paginator(kwiaty_list, 5)
#   products = paginator.page(page)

  if request.method == 'POST':
    nazwa_kwiatu = request.POST.get('nazwa_kwiatu')
    grupy_json = request.POST.get('grupy-json')
    grupy_json_string = json.dumps(grupy_json)
    nowy_kwiat = Kwiat(name=nazwa_kwiatu, kategorie_i_kolory=grupy_json_string)
    nowy_kwiat.save()
    return HttpResponseRedirect(reverse('datatables'))

  context = {
    'segment'  : 'datatables',
    'parent'   : 'apps',
    'kwiaty' : kwiaty_list,
    'kolory' : kolory,
    'kolor_hex' : kolor_hex,
  }
  
  return render(request, 'apps/datatables.html', context)


# Create your views here.
# @login_required(login_url='/users/signin/')
def kolory(request):
  kolory = Kolory.objects.all()
  form = KoloryForm()

#   page = request.GET.get('page', 1)
#   paginator = Paginator(kolory_list, 5)
#   kolory = paginator.page(page)

  if request.method == 'POST':
      form = KoloryForm(request.POST)
      
      nazwa = request.POST.get('name')
      hex_kolor = request.POST.get('hex_kolor')
      kolor = Kolory()
      kolor.custom_background = request.FILES.get('tlo')
      kolor.name = nazwa
      kolor.hex_kolor = hex_kolor
      
      kolor.save()
      return HttpResponseRedirect(reverse('kolory'))
      # if form.is_valid():
          # return post_request_handling(request, form)

  context = {
    'segment'  : 'datatables',
    'parent'   : 'apps',
    'form'     : form,
    'kolory' : kolory
  }
  
  return render(request, 'apps/kolory.html', context)

def kolejnosc(request):
  if request.method == "GET":
    kwiaty = Kwiat.objects.filter(aktywny=True).order_by('kolejnosc')
    return render(request, 'apps/kolejnosc.html', {'kwiaty': kwiaty})
  elif request.method == "POST":
    kolejnosc_idkow = request.POST.get('kolejnosc').split(',')
    for nowe_kolejnosc, idk_kwiatu in enumerate(kolejnosc_idkow):
      kwiat = Kwiat.objects.filter(id=int(idk_kwiatu)).first()
      kwiat.kolejnosc = int(nowe_kolejnosc)
      kwiat.save()
    kwiaty = Kwiat.objects.filter(aktywny=True).order_by('kolejnosc')
    return render(request, 'apps/kolejnosc.html', {'kwiaty': kwiaty})
  else:
    pass


# @login_required(login_url='/users/signin/')
def czytaj_raport(request, id):
  raport = Raport.objects.get(id=id)
  dane = json.loads(raport.wartosc)

  klucze_do_usuniecia = []
  # remove kolors with 0
  for klucz in dane:
    for rodzaj in dane[klucz]:
      for kolor in dane[klucz][rodzaj]:
        if dane[klucz][rodzaj][kolor] == '0':
          klucze_do_usuniecia.append([klucz, rodzaj, kolor])

  # jezeli kwiat nie ma koloru tez usun 
  print(klucze_do_usuniecia)
  for klucze in klucze_do_usuniecia:
    klucz, rodzaj, kolor = klucze 
    del dane[klucz][rodzaj][kolor]


  klucze_do_usuniecia = []
  for klucz in dane:
    for rodzaj in dane[klucz]:
      if len(dane[klucz][rodzaj]) == 0:
          klucze_do_usuniecia.append([klucz, rodzaj])

  print(klucze_do_usuniecia)
  for klucze in klucze_do_usuniecia:
    klucz, rodzaj = klucze 
    del dane[klucz][rodzaj]

  print(dane)
  klucze_do_usuniecia = []
  for key in dane:
    if dane[key] == {}:
      klucze_do_usuniecia.append(key)

  for klucz in klucze_do_usuniecia:
    del dane[klucz]

  kolory = Kolory.objects.all()
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
      
  return render(request, 'apps/czytaj_raport.html', {'raport': raport, 'dane': dane, 'kolor_hex': kolor_hex})


# @login_required(login_url='/users/signin/')
def raport_start(request):
    if request.method == "GET":

      kolory = Kolory.objects.all()
      
      kolor_hex = {}
      for kolor in kolory:
        if kolor.custom_background:
          kolor_hex[kolor.name] = kolor.custom_background.url
        else:
          kolor_hex[kolor.name] = kolor.hex_kolor


      kwiaty = Kwiat.objects.filter(aktywny=True).order_by('kolejnosc')
      for kwiat in kwiaty:
        kwiat.kategorie_i_kolory_list = json.loads(json.loads(kwiat.kategorie_i_kolory))

      # jakbym mial tu gotowego jsona do raportu to moze by bylo łatwiej?

      return render(request, 'apps/raport.html', {'kwiaty': kwiaty, 'kolor_hex': kolor_hex})
    elif request.method == "POST":
      print(request.POST)
      dane = {}
      for field in request.POST:
        if field == 'csrfmiddlewaretoken':
          continue
        kwiat, rodzaj, kolor = field.split('_')
        ilosc = request.POST.get(field)
        if kwiat in dane:
          if rodzaj in dane[kwiat]:
            dane[kwiat][rodzaj][kolor] = ilosc
          else:
            dane[kwiat][rodzaj] = {}
            dane[kwiat][rodzaj][kolor] = ilosc
        else:
          dane[kwiat] = {}
          dane[kwiat][rodzaj] = {}
          dane[kwiat][rodzaj][kolor] = ilosc
      print(dane)
      dane_json = json.dumps(dane)
      raport = Raport(wartosc=dane_json)
      raport.save()
      return HttpResponseRedirect(reverse('lista_raportow'))

    else:
        pass
# @login_required(login_url='/users/signin/')
def lista_raportow(request):
  raporty = Raport.objects.all().order_by('-data_utworzenia')
  print(raporty)
  return render(request, 'apps/lista_raportow.html', {'raporty': raporty})


# @login_required(login_url='/users/signin/')
def delete_kolor(request, id):
    kolor = Kolory.objects.get(id=id)
    kolor.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# @login_required(login_url='/users/signin/')
def update_kolor(request, id):
    update_kolor = Kolory.objects.get(id=id)
    if request.method == 'POST':
        update_kolor.name = request.POST.get('name')
        update_kolor.hex_kolor = request.POST.get('hex_kolor')
        tlo = request.FILES.get('tlo')
        # print(request.POST.get('tlo'))
        # print(type(request.POST.get('tlo')))
        update_kolor.custom_background = tlo
      
        update_kolor.save()
    return redirect(request.META.get('HTTP_REFERER'))

# @login_required(login_url='/users/signin/')
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))


# @login_required(login_url='/users/signin/')
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))


# @login_required(login_url='/users/signin/')
def zmien_status(request, id):
    kwiat = Kwiat.objects.get(id=id)
    if kwiat.aktywny:
        kwiat.aktywny = False
    else:
        kwiat.aktywny = True

    kwiat.save()
    return redirect(request.META.get('HTTP_REFERER'))



# @login_required(login_url='/users/signin/')
def delete_kwiat(request, id):
    kwiat = Kwiat.objects.get(id=id)
    kwiat.delete()
    return redirect(request.META.get('HTTP_REFERER'))



# @login_required(login_url='/users/signin/')
def edytuj_kwiat(request, id):
    if request.method == 'GET':
        kwiat = Kwiat.objects.get(id=id)
        kolory = Kolory.objects.all()
        kwiat.kategorie_i_kolory_list = json.loads(json.loads(kwiat.kategorie_i_kolory))
        kolor_hex = {}
        for kolor in kolory:
            kolor_hex[kolor.name] = kolor.hex_kolor

        return render(request, 'apps/edytuj_kwiat.html', {'kwiat': kwiat, 'kolory': kolory})
    elif request.method == 'POST':
        nazwa_kwiatu = request.POST.get('nazwa_kwiatu')
        grupy_json = request.POST.get('grupy-json')
        grupy_json_string = json.dumps(grupy_json)
        kwiat = Kwiat.objects.filter(id=id).first()
        kwiat.name = nazwa_kwiatu
        kwiat.kategorie_i_kolory = grupy_json_string
        kwiat.save()
        messages.success(request, 'Kwiat zaktualizowany!')
        return HttpResponseRedirect(reverse('datatables'))



# @login_required(login_url='/users/signin/')
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = int(request.POST.get('price'))
        product.info = request.POST.get('info')
        product.save()
    return redirect(request.META.get('HTTP_REFERER'))