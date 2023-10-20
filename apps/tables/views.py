from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from apps.tables.forms import ProductForm, KoloryForm
from apps.common.models import Product, Kolory, Kwiat
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from apps.tables.utils import product_filter
import json

# Create your views here.
# @login_required(login_url='/users/signin/')
def datatables(request):
#   filters = product_filter(request)
  kwiaty_list = Kwiat.objects.all()
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
  kolory_list = Kolory.objects.all()
  form = KoloryForm()

  page = request.GET.get('page', 1)
  paginator = Paginator(kolory_list, 5)
  kolory = paginator.page(page)

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
def update_product(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.price = int(request.POST.get('price'))
        product.info = request.POST.get('info')
        product.save()
    return redirect(request.META.get('HTTP_REFERER'))