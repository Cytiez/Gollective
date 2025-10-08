from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
import datetime

from .models import Product
from .forms import ProductForm


def _is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest' or \
           ('application/json' in request.headers.get('accept', ''))


def _product_to_dict(p: Product):
    return {
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'description': p.description,
        'thumbnail': p.thumbnail,
        'category': p.category,
        'category_display': p.get_category_display(),
        'is_featured': p.is_featured,
        'club_name': p.club_name,
        'season': p.season,
        'release_year': p.release_year,
        'condition': p.condition,
        'authenticity': p.authenticity,
        'user_id': p.user_id,
    }


@login_required(login_url='/login')
def show_main(request):
    # Produk di-load via AJAX (template hanya butuh CURRENT_USER_ID & last_login)
    context = {
        'last_login': request.COOKIES.get('last_login', 'Never'),
        'current_user_id': request.user.id,
    }
    return render(request, "main.html", context)


# ===== JSON LIST & DETAIL (AJAX) =====

@login_required(login_url='/login')
def show_json(request):
    filter_type = request.GET.get('filter', 'all')
    qs = Product.objects.all() if filter_type != 'my' else Product.objects.filter(user=request.user)
    data = [_product_to_dict(p) for p in qs.order_by('-id')]
    return JsonResponse(data, safe=False)

@login_required(login_url='/login')
def show_json_by_id(request, id: int):
    p = get_object_or_404(Product, pk=id)
    return JsonResponse(_product_to_dict(p))


# ===== CRUD AJAX =====

@login_required(login_url='/login')
@require_POST
def add_product_ajax(request):
    name = strip_tags((request.POST.get("name") or "").strip())
    description = strip_tags((request.POST.get("description") or "").strip())
    thumbnail = strip_tags((request.POST.get("thumbnail") or "").strip())
    category = strip_tags(request.POST.get("category") or "home")
    club_name = strip_tags((request.POST.get("club_name") or "").strip())
    season = strip_tags((request.POST.get("season") or "").strip())
    condition = strip_tags(request.POST.get("condition") or "mint")
    is_featured = request.POST.get("is_featured") in ("on", "true", "1", "True")
    authenticity = request.POST.get("authenticity") in ("on", "true", "1", "True")

    try:
        price = int(request.POST.get("price") or "0")
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Price must be an integer.'}, status=400)

    release_year = None
    if (ry := (request.POST.get("release_year") or "").strip()):
        try:
            release_year = int(ry)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Release year must be a number.'}, status=400)

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required.'}, status=400)

    product = Product.objects.create(
        name=name, price=price, description=description, thumbnail=thumbnail,
        category=category, is_featured=is_featured, club_name=club_name, season=season,
        release_year=release_year, condition=condition, authenticity=authenticity,
        user=request.user
    )
    return JsonResponse({'success': True, 'data': _product_to_dict(product)}, status=201)


@login_required(login_url='/login')
@require_POST
def update_product_ajax(request, id: int):
    product = get_object_or_404(Product, pk=id)
    if product.user_id != request.user.id:
        return HttpResponseForbidden("You are not allowed to edit this item.")

    name = strip_tags((request.POST.get("name", product.name)).strip())
    description = strip_tags((request.POST.get("description", product.description)).strip())
    thumbnail = strip_tags((request.POST.get("thumbnail", product.thumbnail)).strip())
    category = strip_tags(request.POST.get("category", product.category))
    club_name = strip_tags((request.POST.get("club_name", product.club_name)).strip())
    season = strip_tags((request.POST.get("season", product.season)).strip())
    condition = strip_tags(request.POST.get("condition", product.condition))

    is_featured = request.POST.get("is_featured")
    authenticity = request.POST.get("authenticity")
    if is_featured is not None:
        product.is_featured = is_featured in ("on", "true", "1", "True")
    if authenticity is not None:
        product.authenticity = authenticity in ("on", "true", "1", "True")

    if (pr := request.POST.get("price")) is not None:
        try:
            product.price = int(pr)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Price must be an integer.'}, status=400)

    if (ry := request.POST.get("release_year")) is not None:
        product.release_year = None
        if ry.strip():
            try:
                product.release_year = int(ry)
            except ValueError:
                return JsonResponse({'success': False, 'message': 'Release year must be a number.'}, status=400)

    if not name:
        return JsonResponse({'success': False, 'message': 'Name is required.'}, status=400)

    product.name = name
    product.description = description
    product.thumbnail = thumbnail
    product.category = category
    product.club_name = club_name
    product.season = season
    product.condition = condition
    product.save()

    return JsonResponse({'success': True, 'data': _product_to_dict(product)})


@login_required(login_url='/login')
@require_POST
def delete_product_ajax(request, id: int):
    product = get_object_or_404(Product, pk=id)
    if product.user_id != request.user.id:
        return HttpResponseForbidden("You are not allowed to delete this item.")
    product.delete()
    return JsonResponse({'success': True, 'id': id})


# ===== Endpoint lama (fallback) =====

@login_required(login_url='/login')
def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect("main:show_main")
    return render(request, "add_product.html", {'form': form})

@login_required(login_url='/login')
def show_product(request, id: int):
    product = get_object_or_404(Product, pk=id)
    return render(request, "product_detail.html", {"product": product})

def show_xml(request):
    xml = serializers.serialize("xml", Product.objects.all())
    return HttpResponse(xml, content_type="application/xml")


# ===== Auth AJAX-aware =====

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if _is_ajax(request):
                return JsonResponse({'success': True, 'redirect': reverse('main:login')})
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        else:
            if _is_ajax(request):
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if _is_ajax(request):
                response = JsonResponse({'success': True, 'redirect': reverse("main:show_main")})
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            if _is_ajax(request):
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST' or _is_ajax(request):
        logout(request)
        response = JsonResponse({'success': True, 'redirect': reverse('main:login')})
        response.delete_cookie('last_login')
        return response
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response
