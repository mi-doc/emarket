from django import forms
from django.contrib import admin
from django.contrib.contenttypes import admin as c_admin
from django.db import models
from django.urls import reverse
from django.utils.html import format_html
import os

from .models import Product, ProductImage
from comments.models import Comment


class CommentAdmin(c_admin.GenericTabularInline):
    model = Comment
    extra = 0
    fields = ('user', 'content')
    readonly_fields = [
        'user',
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('img', 'is_main')

    def get_fields(self, request, obj=None):
        return [
            'img',
            'image',
            'product',
            'is_active',
            'is_main'
        ]

    def img(self, obj):
        return format_html(f'<img src="{obj.image.url}" max-height="100px" width="100px"/>')




class ProductAdminForm(forms.ModelForm):
    Main_image = forms.ChoiceField(required=False, help_text='Main image of the product to show on product card')

    def __init__(self, *args, **kwargs):
        super(ProductAdminForm, self).__init__(*args, **kwargs)
        self.fields['slug'].widget.attrs['disabled'] = True

        self.product = kwargs.get('instance', None)
        if self.product:
            image_choices = [(p.id, os.path.basename(p.image.url)) for p in self.product.get_product_images()]
            self.fields['Main_image'].choices = image_choices
            self.fields['Main_image'].required = False

    def save(self, commit=True):
        main_image_id = self.cleaned_data.get('Main_image', None)
        if main_image_id:
            self.product.set_main_img(main_img_id=main_image_id)
        return super(ProductAdminForm, self).save(commit=commit)

    class Meta:
        model = Product
        fields = '__all__'
        labels = {
            'name': 'Name'
        }
        help_texts = {
            'slug': 'This field is generated automatically',
            'name': "Full name of the product",
            'price': 'Price in RUB',
            'screen_resolution': "Use 'x' as separator. Example: 2160x1620",
            'discount': 'Discount for the product if present. In percent.',
            'other_specifications': 'Any additional info of the product',
        }


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    form = ProductAdminForm
    inlines = [ProductImageInline, CommentAdmin]
    list_display = [
        'id',
        'product_name',
        'image_tag',
        'price',
        'discount',
        'os',
        '_short_description',
        'diagonal',
        'screen_resolution',
        'ram',
        'processor',
        'built_in_memory',
        'main_camera',
        '_other_specifications',
        'created',
        'updated'
    ]

    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(
            attrs={'rows': 7,
                   'cols': 60,
                   })},
    }

    def product_name(self, obj):
        url = reverse('admin:products_product_change', args=(obj.id,))
        return format_html(f'<a href="{url}">{obj.name}</a>')

    def image_tag(self, obj):
        return format_html(f'<img src="{obj.get_main_img_url()}"  height="60" />')

    def _short_description(self, obj):
        text = obj.short_description
        return (text[:75] + '...') if len(text) > 75 else text

    def _other_specifications(self, obj):
        text = obj.other_specifications
        return (text[:75] + '...') if len(text) > 75 else text

    image_tag.short_description = 'Main image'

