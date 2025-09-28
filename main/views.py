from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse

@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")
    
    if filter_type == "all":
        products = Product.objects.all()
    else:
        products = Product.objects.filter(user=request.user)
        
    context = {
        "products": products,
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'user': request.user.username,
    }
    return render(request, "main.html", context)

@login_required(login_url='/login')
def add_product(request):
    form = ProductForm(request.POST or None)
    
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit= False)
        product_entry.user = request.user
        product_entry.save()
        return redirect("main:show_main")
    
    context = {
        'form': form
    }
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def show_product(request, id: int):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def show_xml(request):
    data = Product.objects.all()
    xml = serializers.serialize("xml", data)
    return HttpResponse(xml, content_type="application/xml")

def show_json(request):
    data = Product.objects.all()
    js = serializers.serialize("json", data)
    return HttpResponse(js, content_type="application/json")

def show_xml_by_id(request, id: int):
    obj = get_object_or_404(Product, pk=id)
    xml = serializers.serialize("xml", [obj])  # butuh iterable
    return HttpResponse(xml, content_type="application/xml")

def show_json_by_id(request, id: int):
    obj = get_object_or_404(Product, pk=id)
    js = serializers.serialize("json", [obj])  # butuh iterable
    return HttpResponse(js, content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response

   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

@login_required(login_url='/login/')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this item.")

    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    return render(request, 'edit_product.html', {'form': form, 'product': product})

@login_required(login_url='/login/')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)
    if product.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this item.")

    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))
