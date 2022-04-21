from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Max, Min
from django.db.models.signals import pre_save
from django.urls import reverse
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from rest_framework.reverse import reverse as api_reverse

from comments.models import Comment
from .utils import unique_slug_generator


class Product(models.Model):
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    slug = models.SlugField(default=None, blank=True, null=True)
    name = models.CharField(max_length=64, blank=True, null=True, default=None, verbose_name="Products")
    price = models.IntegerField(null=True, default=0, verbose_name="Price")
    discount = models.IntegerField(null=True, default=0, verbose_name="(%) disc.")
    short_description = models.TextField(null=True, max_length=300, blank=True, default=None)
    diagonal = models.DecimalField(null=True, max_digits=5, decimal_places=1, blank=True, default=None,
                                   verbose_name="Diagonal (\")")
    built_in_memory = models.IntegerField(null=True, blank=True, default=None, verbose_name="Memory (Gb)")
    ram = models.IntegerField(null=True, blank=True, default=None, verbose_name="Ram (Gb)")
    os = models.CharField(null=True, max_length=30, blank=True, default=None)
    screen_resolution = models.CharField(null=True, max_length=10, blank=True, default=None)
    processor = models.CharField(null=True, max_length=30, blank=True, default=None)
    main_camera = models.IntegerField(null=True, blank=True, default=None, verbose_name="Camera (Mpx)")
    other_specifications = models.TextField(null=True, blank=True, default=None)

    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s, %s" % (self.price, self.name)

    def get_main_img_url(self):
        """
        Returns url of the main image of Product
        """
        img = ProductImage.objects.filter(product=self, is_main=True).first()
        if not img:
            # If the product doesn't have main image, we take the first image and make it main
            img = ProductImage.objects.filter(product=self).first()
            if not img:
                return None
            img.is_main = True
            img.save()
        return img.image.url

    def set_main_img(self, main_img_id=None):
        """
        Setting maing image for product
        :param main_img_id: id of a particular product image to become the main image of a product
        :return: nothing
        """
        pr_images = self.get_product_images()
        if not main_img_id: return
        if not pr_images.filter(id=main_img_id): return

        for image in pr_images:
            image.is_main = False
            image.save()

        main_image = pr_images.get(id=main_img_id)
        main_image.is_main = True
        main_image.save()

    def get_product_images(self):
        """
        Returns a queryset of images attached to the product
        """
        return ProductImage.objects.filter(product=self)

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
        """
        Returns absolute url of a product
        :return: url
        """
        return reverse("products:product", kwargs={"slug": self.slug})

    def get_api_url(self, request=None):
        return api_reverse("api:product-rud", kwargs={'pk': self.pk}, request=request)

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
        """
        Return content type
        :return: content type
        """
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    @classmethod
    def get_distinct_values_from_field(cls, field):
        """
        Returns a list of all distinct values of a specified field of product
        (like all processors in all available products)
        :param field: a field to get values for
        :return: a list of values
        """
        values = list(cls.objects.all().values_list(field).order_by(field).distinct())
        if (None,) in values:
            values.remove((None,))
        return values

    @classmethod
    def get_field_choices(cls, field):
        """
        Returns a tuple with choices for a form field
        :param field: a field to get choices for
        :return: a tuple with choices
        """
        val = cls.get_distinct_values_from_field(field)
        return ((v[0], v[0]) for v in val)

    @classmethod
    def get_max_price(cls):
        """
        Returns price of a most expencive product
        :return: integer
        """
        return cls.objects.aggregate(max=Max('price'))['max'] or 0

    @classmethod
    def get_min_price(cls):
        """
        Returns price of the cheapest product
        :return: integer
        """
        return cls.objects.aggregate(min=Min('price'))['min'] or 0

    @classmethod
    def get_max_memory(cls):
        """
        Returns the biggest built-in memory of all products
        :return: integer
        """
        return cls.objects.aggregate(max=Max('built_in_memory'))['max'] or 0

    @classmethod
    def get_min_memory(cls):
        """
        Returns the smallest built-in memory of all products
        :return: integer
        """
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
