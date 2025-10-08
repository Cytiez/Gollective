from django.urls import path
from .views import (
    show_main, add_product, show_product,
    show_xml, show_json, show_json_by_id,
    register, login_user, logout_user,
    add_product_ajax, update_product_ajax, delete_product_ajax,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),

    # Fallback render (kalau dibutuhkan)
    path("create/", add_product, name="add_product"),
    path("product/<int:id>/", show_product, name="show_product"),

    # JSON untuk AJAX
    path("json/", show_json, name="show_json"),
    path("json/<int:id>/", show_json_by_id, name="show_json_by_id"),
    path("xml/", show_xml, name="show_xml"),

    # Auth
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),

    # AJAX CRUD endpoints
    path('product/create-ajax/', add_product_ajax, name='add_product_ajax'),
    path('product/<int:id>/update-ajax/', update_product_ajax, name='update_product_ajax'),
    path('product/<int:id>/delete-ajax/', delete_product_ajax, name='delete_product_ajax'),
]
