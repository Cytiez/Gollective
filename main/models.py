from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home Jersey'),
        ('away', 'Away Jersey'),
        ('third', 'Third Jersey'),
    ]

    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='home')
    is_featured = models.BooleanField(default=False)

    # ekstra (vintage)
    club_name = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=20, blank=True)
    release_year = models.IntegerField(blank=True, null=True)
    condition = models.CharField(max_length=50, default="Mint")
    authenticity = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.club_name} {self.season} - {self.name}"
