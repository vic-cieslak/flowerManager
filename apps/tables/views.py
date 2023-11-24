from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from apps.tables.forms import  KoloryForm
from apps.common.models import Zamowienie, Kolory, Kwiat, Raport
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.tables.utils import product_filter
import json
from django.contrib import messages
from django.db.models.functions import Lower
from django.utils.html import format_html

def remove_zeros(d):
    keys_to_delete = []
    for key, value in d.items():
        if isinstance(value, dict):
            d[key] = remove_zeros(value)
        elif value == 0:
            keys_to_delete.append(key)
    for key in keys_to_delete:
        del d[key]
    return {k: v for k, v in d.items() if v}  # Remove empty dictionaries


# Create your views here.
@login_required(login_url='/users/signin/')
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
    print(kwiat)
    kwiat.kategorie_i_kolory_list = kwiat.kategorie_i_kolory


  page = request.GET.get('page', 1)
#   paginator = Paginator(kwiaty_list, 5)
#   products = paginator.page(page)

  if request.method == 'POST':
    nazwa_kwiatu = request.POST.get('nazwa_kwiatu')
    grupy_json = request.POST.get('grupy-json')
    grupy_json_dict = json.loads(grupy_json)
    nowy_kwiat = Kwiat(name=nazwa_kwiatu, kategorie_i_kolory=grupy_json_dict)
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
@login_required(login_url='/users/signin/')
def kolory(request):
  kolory = Kolory.objects.all().order_by('name')
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
@login_required(login_url='/users/signin/')
def kolejnosc(request):
  if request.method == "GET":
    kwiaty = Kwiat.objects.filter(aktywny=True).order_by('kolejnosc')
    return render(request, 'apps/kolejnosc.html', {'kwiaty': kwiaty})
  elif request.method == "POST":
    print(request.POST.get('kolejnosc'))
    kolejnosc_idkow = request.POST.get('kolejnosc').split(',')
    for nowe_kolejnosc, idk_kwiatu in enumerate(kolejnosc_idkow):
      kwiat = Kwiat.objects.filter(id=int(idk_kwiatu)).first()
      kwiat.kolejnosc = int(nowe_kolejnosc)
      kwiat.save()
    kwiaty = Kwiat.objects.filter(aktywny=True).order_by('kolejnosc')
    return render(request, 'apps/kolejnosc.html', {'kwiaty': kwiaty})
  else:
    pass


@login_required(login_url='/users/signin/')
def czytaj_raport(request, id):
  raport = Raport.objects.get(id=id)
  dane = raport.wartosc
  if type(dane) == str:
    dane = json.loads(raport.wartosc)

  # print(dane)
  kolory = Kolory.objects.all()
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
  # print(dane)
  def sort_dict(d):
      if isinstance(d, dict):
          return {k: sort_dict(d[k]) for k in sorted(d)}
      return d


  sorted_dane = sort_dict(dane)

  return render(request, 'apps/czytaj_raport.html', {'raport': raport, 'dane': sorted_dane, 'kolor_hex': kolor_hex})


@login_required(login_url='/users/signin/')
def czytaj_raport_do_kupienia(request, id):
  raport = Raport.objects.get(id=id)
  dane = raport.wartosc
  if type(dane) == str:
    dane = json.loads(raport.wartosc)

  # print(dane)
  kolory = Kolory.objects.all()
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
  # print(dane)
  def sort_dict(d):
      if isinstance(d, dict):
          return {k: sort_dict(d[k]) for k in sorted(d)}
      return d


  sorted_dane = sort_dict(dane)
  def remove_zeros_and_negatives_from_dict(d):
      if isinstance(d, dict):
          return {k: remove_zeros_and_negatives_from_dict(v) for k, v in d.items() if v not in [0, -1] and remove_zeros_and_negatives_from_dict(v)}
      else:
          return d

  dane = remove_zeros_and_negatives_from_dict(sorted_dane) 
  return render(request, 'apps/czytaj_raport.html', {'tylko_do_kupienia': True, 'raport': raport, 'dane': dane, 'kolor_hex': kolor_hex})


@login_required(login_url='/users/signin/')
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
        kwiat.kategorie_i_kolory_list = kwiat.kategorie_i_kolory

      # jakbym mial tu gotowego jsona do raportu to moze by bylo łatwiej?
      # cloned_kwiaty = [kwiat for kwiat in kwiaty for _ in range(10)]
      # kwiaty = cloned_kwiaty
      return render(request, 'apps/raport.html', {'kwiaty': kwiaty, 'kolor_hex': kolor_hex})
    elif request.method == "POST":
      data = json.loads(request.body)
      print(data)
      # dane_json = json.loads(data)
      raport = Raport(wartosc=data)
      raport.save()
      return HttpResponseRedirect(reverse('lista_raportow'))

    else:
        pass

@login_required(login_url='/users/signin/')
def lista_raportow(request):
  raporty = Raport.objects.all().order_by('-data_utworzenia')
  # print(raporty)
  return render(request, 'apps/lista_raportow.html', {'raporty': raporty})


@login_required(login_url='/users/signin/')
def delete_kolor(request, id):
    kolor = Kolory.objects.get(id=id)
    kolor.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def usun_raport(request, id):
    raport = Raport.objects.get(id=id)
    raport.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
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

@login_required(login_url='/users/signin/')
def post_request_handling(request, form):
    form.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def delete_product(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def zmien_status(request, id):
    kwiat = Kwiat.objects.get(id=id)
    if kwiat.aktywny:
        kwiat.aktywny = False
    else:
        kwiat.aktywny = True

    kwiat.save()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/signin/')
def delete_kwiat(request, id):
    kwiat = Kwiat.objects.get(id=id)
    kwiat.delete()
    return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url='/users/signin/')
def edytuj_kwiat(request, id):
    if request.method == 'GET':
        kwiat = Kwiat.objects.get(id=id)
        kolory = Kolory.objects.all()
        kwiat.kategorie_i_kolory_list = kwiat.kategorie_i_kolory
        kolor_hex = {}
        for kolor in kolory:
          if kolor.custom_background:
            kolor_hex[kolor.name] = kolor.custom_background.url
          else:
            kolor_hex[kolor.name] = kolor.hex_kolor
        print(kwiat.kategorie_i_kolory_list)
        
        return render(request, 'apps/edytuj_kwiat.html', {'kwiat': kwiat, 'kolory': kolory, 'kolor_hex':kolor_hex})
    elif request.method == 'POST':
        nazwa_kwiatu = request.POST.get('nazwa_kwiatu')
        grupy_json = request.POST.get('grupy-json')
        grupy_json_dict = json.loads(grupy_json)
        kwiat = Kwiat.objects.filter(id=id).first()
        kwiat.name = nazwa_kwiatu
        kwiat.kategorie_i_kolory = grupy_json_dict
        kwiat.save()
        messages.success(request, 'Kwiat zaktualizowany!')
        return HttpResponseRedirect(reverse('datatables'))
        


@login_required(login_url='/users/signin/')
def edytuj_zamowienie(request, id):

    if request.method == 'GET':
        zamowienie = Zamowienie.objects.filter(id=id).first()
        kwiaty = Kwiat.objects.all()
        kolory = Kolory.objects.all()
        
        kolor_hex = {}
        for kolor in kolory:
          if kolor.custom_background:
            kolor_hex[kolor.name] = kolor.custom_background.url
          else:
            kolor_hex[kolor.name] = kolor.hex_kolor
            
        for kwiat in kwiaty:
          kwiat.kategorie_i_kolory_list = kwiat.kategorie_i_kolory

        return render(request, 'apps/edytuj_zamowienie.html',
         {'kwiaty': kwiaty, 'kolor_hex': kolor_hex, 'zamowienie': zamowienie})

    elif request.method == 'POST':
        z = Zamowienie()
        produkty = request.POST.get('produkty')
        produkty = json.loads(produkty)
        cleaned_produkty = remove_zeros(produkty)
        z.odbiorca = request.POST.get('odbiorca')
        z.produkty = cleaned_produkty
        # z.status = 'Kupione'
        z.termin_dostarczenia = request.POST.get('data')
        z.notatka = request.POST.get('notatka')
        z.zdjecie = request.FILES.get('zdjecie')
        z.save()
        return HttpResponseRedirect(reverse('lista_zamowien'))



@login_required(login_url='/users/signin/')
def lista_zamowien(request):
  zamowienia = Zamowienie.objects.filter(status='').order_by('termin_dostarczenia')

  kolory = Kolory.objects.all()
  
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
  return render(request, 'apps/lista_zamowien.html', 
  {'zamowienia': zamowienia, 'kolor_hex': kolor_hex, 'btn_text': 'Archiwum'})


@login_required(login_url='/users/signin/')
def archiwum_zamowien(request):
  zamowienia = Zamowienie.objects.filter(status='archiwum').order_by('termin_dostarczenia')
  kolory = Kolory.objects.all()
  
  kolor_hex = {}
  for kolor in kolory:
    if kolor.custom_background:
      kolor_hex[kolor.name] = kolor.custom_background.url
    else:
      kolor_hex[kolor.name] = kolor.hex_kolor
  return render(request, 'apps/lista_zamowien.html', 
  {'zamowienia': zamowienia, 'kolor_hex': kolor_hex, 'btn_text': 'Przywróć'})



@login_required(login_url='/users/signin/')
def usun_zamowienie(request, id):
    zamowienie = Zamowienie.objects.get(id=id)
    zamowienie.delete()
    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/users/signin/')
def przenies_do_archiwum(request, id):
    zamowienie = Zamowienie.objects.get(id=id)
    status = zamowienie.status

    if status == 'archiwum':
      zamowienie.status = ''
    else:
      zamowienie.status = 'archiwum'

    zamowienie.save()

    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/users/signin/')
def zmien_status_zamowienia(request, id):
    zamowienie = Zamowienie.objects.get(id=id)
    if 'HX-Request' in request.headers:
        # Return a simple string response

        print(request.GET)
        nazwa = request.GET.get('nazwa')
        rodzaj = request.GET.get('rodzaj')
        kolor = request.GET.get('kolor')
        new_status = request.GET.get('new_status')
        zamowienie.produkty[nazwa][rodzaj][kolor]['status'] = new_status
        zamowienie.save()

        if new_status == 'kupione':
          style = "color: #fdec34;font-weight: bold; width: 90px"
        elif new_status == 'odebrane':
          style = "color: #3499fd;font-weight: bold; width: 90px"
        elif new_status == 'odłożone':
          style = "color: #12ff26;font-weight: bold; width: 90px;"
        elif new_status == '':
          style = "color: white; width: 90px;"

        # Create the span element with the custom class and new status
        if not new_status:
          new_status = 'brak statusu'
        span_html = format_html('<div style="{}">{}</div>', style, new_status)
        return HttpResponse(span_html)

    else:
      pass



@login_required(login_url='/users/signin/')
def dodaj_zamowienie(request, id=None):
    if request.method == 'GET':
        kwiaty = Kwiat.objects.all()
        kolory = Kolory.objects.all()
        
        kolor_hex = {}
        for kolor in kolory:
          if kolor.custom_background:
            kolor_hex[kolor.name] = kolor.custom_background.url
          else:
            kolor_hex[kolor.name] = kolor.hex_kolor
            
        for kwiat in kwiaty:
          kwiat.kategorie_i_kolory_list = kwiat.kategorie_i_kolory

        return render(request, 'apps/dodaj_zamowienie.html', {'kwiaty': kwiaty, 'kolor_hex': kolor_hex})
    elif request.method == 'POST':
        z = Zamowienie()
        produkty = request.POST.get('produkty')
        produkty = json.loads(produkty)
        cleaned_produkty = remove_zeros(produkty)
        z.odbiorca = request.POST.get('odbiorca')
        z.produkty = cleaned_produkty
        # z.status = 'Kupione'
        z.termin_dostarczenia = request.POST.get('data')
        z.notatka = request.POST.get('notatka')
        z.zdjecie = request.FILES.get('zdjecie')
        z.save()
        return HttpResponseRedirect(reverse('lista_zamowien'))

@login_required(login_url='/users/signin/')
def odswiez_kolory(request, id):
  kwiat = Kwiat.objects.get(id=id)
  kolory = Kolory.objects.all()
  nazwy_kolorow = [kolor.name for kolor in kolory]
  kategorie_i_kolory_list = kwiat.kategorie_i_kolory
  # print(kategorie_i_kolory_list)
  for kwiat_ in kategorie_i_kolory_list:
    for kolor in kwiat_['kolory']:
      if kolor not in nazwy_kolorow:
          print('removing ', kolor)
          kwiat_['kolory'].remove(kolor)

  # print('nowe : ', kategorie_i_kolory_list)
  # nowe = json.dumps(kategorie_i_kolory_list)

  # print('nowe_string', nowe)
  # print(type(nowe))
  # print('nowe nowe ', json.dumps(nowe))
  # nowe_nowe = json.dumps(nowe)
  kwiat.kategorie_i_kolory = kategorie_i_kolory_list 
  kwiat.save()

  return HttpResponseRedirect(reverse('edytuj_kwiat', kwargs={'id': id}))

@login_required(login_url='/users/signin/')
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = int(request.POST.get('price'))
        product.info = request.POST.get('info')
        product.save()
    return redirect(request.META.get('HTTP_REFERER'))