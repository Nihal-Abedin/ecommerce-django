from django.shortcuts import render

from store.serializer import ProductSerializer, CategorySerializer, CartSerializer, CartOrderItemSerializer, \
    CartOrderSerializer

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from store.models import Category, Products, Tax, Gallery, Specification, Size, Coupon, Color, Cart, CartOrderItem, \
    CartOrder, ProductsFaq, Review, Wishtlist, Notifications

from user_auths.models import User

from decimal import Decimal
from rest_framework.response import Response


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class ProductsListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]


class ProductDetailView(generics.RetrieveAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        return Products.objects.get(slug=slug)


class CartAPIView(generics.ListCreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        payload = request.data

        product_id = payload['product_id']
        user_id = payload['user_id']
        qty = payload['qty']
        price = payload['price']
        shipping_amount = payload['shipping_amount']
        country = payload['country']
        size = payload['size']
        color = payload['color']
        cart_id = payload['cart_id']

        product = Products.objects.get(id=product_id)

        if user_id != 'undefined':
            user = User.objects.get(id=user_id)
        else:
            user = None
        tax = Tax.objects.filter(country=country).first()

        if tax:
            tax_rate = tax.rate / 100
        else:
            tax_rate = 0

        cart = Cart.objects.filter(cart_id=cart_id, product=product).first()

        if cart:
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = Decimal(tax_rate) * int(qty)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id
            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee

            cart.save()

            return Response({'message': 'Cart Updated Successfully'}, status=status.HTTP_200_OK)
        else:
            cart = Cart()
            cart.product = product
            cart.user = user
            cart.qty = qty
            cart.price = price
            cart.sub_total = Decimal(price) * int(qty)
            cart.shipping_amount = Decimal(shipping_amount) * int(qty)
            cart.tax_fee = Decimal(tax_rate) * int(qty)
            cart.color = color
            cart.size = size
            cart.country = country
            cart.cart_id = cart_id
            service_fee_percentage = 10 / 100
            cart.service_fee = Decimal(service_fee_percentage) * cart.sub_total

            cart.total = cart.sub_total + cart.shipping_amount + cart.service_fee + cart.tax_fee

            cart.save()

            return Response({'message': 'Cart Created Successfully'}, status=status.HTTP_201_CREATED)

class CartListView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    queryset = Cart.objects.all()

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.filter(id=user_id)
            queryset = Cart.objects.filter(user=user_id, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_queryset(self):
        cart_id = self.kwargs['cart_id']
        user_id = self.kwargs.get('user_id')

        if user_id is not None:
            user = User.objects.filter(id=user_id)
            queryset = Cart.objects.filter(user=user_id, cart_id=cart_id)
        else:
            queryset = Cart.objects.filter(cart_id=cart_id)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset  = self.get_queryset()
        
        total_shipping = 0.0
        total_tax = 0.0
        total_service_fee = 0.0
        total_sub_total = 0.0
        total_total = 0.0

        for cart_item in queryset:
            total_shipping += float(cart_item.shipping_amount)
            total_tax += float(cart_item.tax_fee)
            total_service_fee += float(cart_item.service_fee)
            total_sub_total += float(cart_item.sub_total)
            total_total += float(cart_item.total)

        data = {
            'shipping': total_shipping,
            'tax': total_tax,
            'service_fee': total_service_fee,
            'sub_total':total_sub_total,
            'total':total_total
        }

        return Response(data)
    
class CartItemDeleteView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get_object(self):
        cart_id = self.kwargs['cart_id']
        item_id = self.kwargs['item_id']
        user_id = self.kwargs.get('user_id')

        if user_id:
            user = User.objects.get(id=user_id)
            cart = Cart.objects.get(id=item_id, cart_id = cart_id, user = user)
        else:
            cart = Cart.objects.get(id=item_id, cart_id = cart_id)

        return cart
    
    Response({'message': 'Cart Deleted Successfully'}, status=status.HTTP_204_NO_CONTENT)

    