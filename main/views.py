from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from .models import Product
from .forms import ProductForm

def show_main(request):
    products = Product.objects.all()
    context = {
        "npm": "2406496025",
        "name": "Raqilla Al-Abrar",
        "class": "PBP A",
        "products": products,
    }
    return render(request, "main.html", context)

def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_main")
    return render(request, "add_product.html", {"form": form})

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
