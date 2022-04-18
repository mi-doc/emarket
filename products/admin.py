from django.contrib import admin
from django.db import models
from .models import Product, ProductImage
from django.utils.html import format_html
from django.urls import reverse
from django import forms


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0
    readonly_fields = ('img',)

    def get_fields(self, request, obj=None):
        return [
            'img',
            'image',
            'product',
            'is_active'
        ]

    def img(self, obj):
        return format_html(f'<img src="{obj.image.url}" max-height="100px" width="100px"/>')



class ProjectAdminForm(forms.ModelForm):

    Main_image = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(ProjectAdminForm, self).__init__(*args, **kwargs)
        self.product = kwargs['instance']
        image_choices = [(p.id, p.image.url) for p in kwargs['instance'].get_product_images()]
        self.fields['Main_image'].choices = image_choices
        self.fields['Main_image'].required = False

    def save(self, commit=True):
        pr_images = ProductImage.objects.filter(product=self.product)
        for image in pr_images:
            image.is_main = False
            image.save()
        Main_image_id = self.cleaned_data.get('Main_image', None)
        main_image = pr_images.get(id=Main_image_id)
        main_image.is_main = True
        main_image.save()
        return super(ProjectAdminForm, self).save(commit=commit)

    class Meta:
        model = Product
        fields = '__all__'


@admin.register(Product)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]
    list_display.remove('slug')
    list_display[1] = 'product_name'
    list_display.insert(2, 'image_tag')

    def product_name(self, obj):
        url = reverse('admin:products_product_change', args=(obj.id,))
        return format_html(f'<a href="{url}">{obj.name}</a>')

    def image_tag(self, obj):
        print(obj.get_main_img_url())
        return format_html(f'<img src="{obj.get_main_img_url()}"  height="60" />')
    image_tag.short_description = 'Main image'

    form = ProjectAdminForm
    inlines = [ProductImageInline]
