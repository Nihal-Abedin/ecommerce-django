from rest_framework import serializers

from store.models import Category, Products, Gallery, Specification, Size, Coupon, Color, Cart, CartOrderItem, \
    CartOrder, ProductsFaq, Review, Wishtlist, Notifications

from vendor.models import Vendor


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        # fields = '__all__'
        exclude = ['id']


class CartOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CartOrderSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CartOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartOrderItem
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CartOrderItemSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super(CartSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3

    class Meta:
        model = Cart
        fields = '__all__'


class ProductFAQtSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsFaq
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProductFAQtSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(VendorSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ReviewSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishtlist
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(WishlistSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(NotificationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CouponSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.methods == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 3


class ProductSerializer(serializers.ModelSerializer):
    gallery = GallerySerializer(many=True, read_only=True)
    color = ColorSerializer(many=True, read_only=True)
    specifications = SpecificationSerializer(many=True, read_only=True)
    size = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Products
        fields = ['id', 'title', 'image', 'category', 'description', 'price',
                  'old_price',
                  'shipping_amount',
                  'stock_qty',
                  'in_stock',
                  'gallery', 'color', 'specifications',
                  'size',
                  'featured',
                  'status',
                  'views',
                  'rating',
                  'vendor',
                  'product_rating',
                  'ratings_count',
                  'pid',
                  'slug',
                  'date']

    def __init__(self, *args, **kwargs):
        super(ProductSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')

        if request and request.method == 'POST':
            self.Meta.depth = 0
        else:
            self.Meta.depth = 2
