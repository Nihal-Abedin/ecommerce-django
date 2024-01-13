from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    rating = models.PositiveIntegerField(default=0, null=True, blank=True)
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

    def product_rating(self):
        product_rating = Review.objects.filter(product=self).aggregate(avg_rating=models.Avg('rating'))
        return product_rating['avg_rating']

    def ratings_count(self):
        return Review.objects.filter(product=self).count()

    def gallery(self):
        return Gallery.objects.filter(product=self)

    def specifications(self):
        return Specification.objects.filter(product=self)

    def size(self):
        return Size.objects.filter(product=self)

    def color(self):
        return Color.objects.filter(product=self)

    def save(self, *args, **kwargs):
        self.rating = self.product_rating()
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


class Cart(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cart_id} - {self.product.title}"


class CartOrder(models.Model):
    PAYMENTS_STATUS = (
        ('paid', "Pain"),
        ('pending', "Pending"),
        ('processing', "Processing"),
        ('canceled', "Canceled"),
    )
    ORDERS_STATUS = (
        ('pending', "Pending"),
        ('fulfilled', "fulfilled"),
        ('canceled', "Canceled"),
    )
    vendor = models.ManyToManyField(Vendor)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    payment_status = models.CharField(choices=PAYMENTS_STATUS, max_length=100, default='pending')
    order_status = models.CharField(choices=ORDERS_STATUS, max_length=100, default='pending')

    # COUPONS
    initial_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    # BIO_DATA
    full_names = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    # SHIPPING ADDRESS
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    oid = ShortUUIDField(unique=True, length=10, alphabet="123456789bcdefg")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


class CartOrderItem(models.Model):
    ORDERS_STATUS = (
        ('pending', "Pending"),
        ('fulfilled', "fulfilled"),
        ('canceled', "Canceled"),
    )
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    order_status = models.CharField(choices=ORDERS_STATUS, max_length=100, default='pending')

    # COUPONS
    initial_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    saved = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)

    oid = ShortUUIDField(unique=True, length=10, alphabet="123456789bcdefg")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid


class ProductsFaq(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)

    question = models.CharField(max_length=1000, null=False, blank=False)
    answer = models.TextField(null=False, blank=False)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

    class Meta:
        verbose_name_plural = 'Products FAQs'


class Review(models.Model):
    RATINGS = (
        (1, "1 star"),
        (2, "2 star"),
        (3, "3 star"),
        (4, "4 star"),
        (5, "5 star"),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=None, choices=RATINGS)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name_plural = 'Products Reviews'

    def profile(self):
        return Profile.objects.get(use=self.user)


@receiver(post_save, sender=Review)
def update_product_rating(sender, instance, **kwargs):
    if instance.product:
        instance.product.save()


class Wishtlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.title


class Notifications(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, blank=True, null=True)
    order_item = models.ForeignKey(CartOrderItem, on_delete=models.SET_NULL, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        if self.order:
            return self.order.oId
        else:
            return f"Notification - {self.pk}"


class Coupon(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    user_by = models.ManyToManyField(User, blank=True)
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.product.title
