from django.forms import ModelForm
from .models import Product

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "name", "price", "description", "thumbnail",
            "category", "is_featured",
            "club_name", "season", "release_year",
            "condition", "authenticity",
        ]
