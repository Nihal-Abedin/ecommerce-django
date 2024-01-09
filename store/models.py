from django.db import models
from user_auths.models import User, Profile
from vendor.models import Vendor
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(default='category.jpg', upload_to='category', null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Categories'


class Products(models.Model):
    STATUS = (
        ('draft', "Draft"),
        ('disabled', "Disabled"),
        ('in_review', "In Review"),
        ('published', "Published"),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    image = models.FileField(default='products.jpg', upload_to='products', null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    old_price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    stock_qty = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=100, choices=STATUS, default='published')
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    pid = ShortUUIDField(unique=True, length=10, alphabet="123456789bcdefg")
    slug = models.SlugField(unique=True, max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = 'Products'

    def save(self, *args, **kwargs):
        if not self.slug or self.slug is None:
            self.slug = slugify(self.title)
        super(Products, self).save(*args, **kwargs)


class Gallery(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    image = models.FileField(default='product.jpg', upload_to='products')
    title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(unique=True, length=10, alphabet="123456789bcdefg")

    def __str__(self):
        return str(self.product.title)

    class Meta:
        verbose_name_plural = 'Galleries'

class Specification(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class Size(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return str(self.name)


class Color(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    color_code = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.name)
