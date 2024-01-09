from django.contrib import admin

from store.models import Category, Products, Gallery, Size, Specification, Color


class GalleryInline(admin.TabularInline):
    model = Gallery


class SizeInline(admin.TabularInline):
    model = Size


class SpecificationInline(admin.TabularInline):
    model = Specification


class ColorInline(admin.TabularInline):
    model = Color


class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "price", "stock_qty", "in_stock", "category", "vendor", "featured"]
    list_editable = ["featured"]
    list_filter = ['date']
    search_fields = ["title"]
    inlines = [GalleryInline, SpecificationInline, SizeInline, ColorInline]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "active"]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Products, ProductAdmin)
