from django.contrib import admin

from .models import Product, ProductImage
from django.utils.html import format_html
from django.urls import reverse

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_display.remove('slug')
    list_display[1] = 'product_name'
    list_display.insert(2, 'image_tag')

    def product_name(self, obj):
        url = reverse('admin:products_product_change', args=(obj.id,))
        return format_html(f'<a href="{url}">{obj.name}</a>')

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.get_main_img_url()}"  height="60" />')
    image_tag.short_description = 'Main image'

    inlines = [ProductImageInline]