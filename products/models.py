from comments.models import Comment
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max, Min
from django.db.models.signals import pre_save
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from rest_framework.reverse import reverse as api_reverse

from .utils import unique_slug_generator


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    slug = models.SlugField(default=None, null=True)
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Products")
    price = models.IntegerField(null=True, default=0, verbose_name="Price")
    discount = models.IntegerField(null=True, default=0, verbose_name="Discount (percent)")
    short_description = models.TextField(null=True, max_length=100, blank=True, default=None)
    diagonal = models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True, default=None,
                                   verbose_name="Diagonal (inches)")
    built_in_memory = models.IntegerField(null=True, blank=True, default=None, verbose_name="Built in memory (Gb)")
    ram = models.IntegerField(null=True, blank=True, default=None, verbose_name="Ram (Gb)")
    os = models.CharField(null=True, max_length=30, blank=True, default=None)
    screen_resolution = models.CharField(null=True, max_length=10, blank=True, default=None)
    processor = models.CharField(null=True, max_length=30, blank=True, default=None)
    main_camera = models.IntegerField(null=True, blank=True, default=None, verbose_name="Main camera (Mpx)")
    other_specifications = models.TextField(null=True, blank=True, default=None)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.price, self.name)

    def get_main_img_url(self):
        """
        Returns main image of Product
        """
        return ProductImage.objects.get(product=self, is_main=True).image.url

    def get_price_with_discount(self):
        """
        Product price with discount (if it has discount)
        """
        try:
            discount_price = self.price - (self.price / 100 * self.discount)
        except:
            discount_price = self.price
        return int(discount_price)

    def get_absolute_url(self):
        return reverse("products:product", kwargs={"slug": self.slug})

    def get_api_url(self, request=None):
        return api_reverse("api:product-rud", kwargs={'pk': self.pk}, request=request)

    @classmethod
    def get_distinct_values_from_field(cls, field):
        values = list(cls.objects.all().values_list(field).order_by(field).distinct())
        if (None,) in values:
            values.remove((None,))
        return values

    @property
    def comments(self):
        """
        Comments of product
        """
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @classmethod
    def get_max_price(cls):
        return cls.objects.aggregate(max=Max('price'))['max'] or 0

    @classmethod
    def get_min_price(cls):
        return cls.objects.aggregate(min=Min('price'))['min'] or 0

    @classmethod
    def get_max_memory(cls):
        return cls.objects.aggregate(max=Max('built_in_memory'))['max'] or 0

    @classmethod
    def get_min_memory(cls):
        return cls.objects.aggregate(min=Min('built_in_memory'))['min'] or 0


def pre_save_product_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        # instance.slug = create_slug(instance)
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pre_save_product_receiver, sender=Product)


class ProductImage(models.Model):
    image = models.ImageField(upload_to='products_images/')
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    if is_main:
        thumbnail = ImageSpecField(source='image',
                                   processors=[ResizeToFit(200, 100)],
                                   format='JPEG',
                                   options={'quality': 60})
    else:
        thumbnail = None

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"
