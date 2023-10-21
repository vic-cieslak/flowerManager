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
      if form.is_valid():
          return post_request_handling(request, form)

  context = {
    'segment'  : 'datatables',
    'parent'   : 'apps',
    'form'     : form,
    'kolory' : kolory
  }
  
  return render(request, 'apps/kolory.html', context)


# @login_required(login_url='/users/signin/')
def raport_start(request):
    # złap wszystkie aktywne kwiaty
    # render dla VUEJS
    # user wypełnia jsona na froncie
        # robi post
        # raport sie dodaje
        # raport do wyswietenia w liscie raportow
    kwiaty = Kwiat.objects.all()
    return render(request, 'apps/raport.html', {'kwiaty': kwiaty})


# @login_required(login_url='/users/signin/')
def lista_raportow(request):
  raporty = Raport.objects.all()

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