import os
from django.test import TestCase
from mixer.backend.django import mixer

from ..models import Product, ProductImage


class ProductTestCase(TestCase):

    def setUp(self):
        product = mixer.blend(Product, os='android', diagonal=7.1, price=10000, discount=10, name='Samsung')
        product.save()

        product2 = mixer.blend(Product, os='ios', diagonal=10, price=21000, discount=5, name='Ipad')
        product2.save()

        product3 = mixer.blend(Product, os='android', diagonal=9.2, price=14000, discount=15, name='Huawei')
        product3.save()

    def tearDown(self):
        for pi in ProductImage.objects.all():
            url = os.getcwd() + pi.image.url
            os.remove(url)

    def test_get_price_with_discount(self):
        product = mixer.blend(Product, price=10000, discount=10)
        product.save()
        discounted_price = int(product.get_price_with_discount())
        self.assertEqual(discounted_price, 9000)

        product = mixer.blend(Product, price=25000, discount=8)
        product.save()
        discounted_price = int(product.get_price_with_discount())
        self.assertEqual(discounted_price, 23000)

    def test_get_distinct_values_from_field(self):
        field = 'diagonal'
        diagonals = list(Product.objects.all().values_list(field))
        result = Product.get_distinct_values_from_field(field)
        self.assertEqual(sorted(diagonals), sorted(result))
        
        product_id = Product.objects.first().id
        result2 = Product.get_distinct_values_from_field(field, product_ids=(product_id,))
        product_diagonal = Product.objects.get(pk=product_id).diagonal
        self.assertEqual(len(result2), 1)
        self.assertEqual((product_diagonal,), result2[0])        



        

    def test___str__(self):
        product = mixer.blend(Product, price=25000, name='meizu mx5')
        product.save()
        self.assertEqual(str(product), '25000, meizu mx5')

    def test_get_main_image_url(self):
        product = Product.objects.first()
        image_main = mixer.blend(ProductImage, product=product, is_main=True)
        image_not_main = mixer.blend(ProductImage, product=product, is_main=False)

        self.assertEqual(
            product.get_main_img_url(),
            image_main.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            image_not_main.image.url
        )

    def test_get_absolute_url(self):
        absolute_url = '/products/iphonex/'

        product = mixer.blend(Product, name='IPhoneX')
        url = product.get_absolute_url()
        self.assertEqual(url, absolute_url)

        product2 = mixer.blend(Product, name='IPhoneX')
        url2 = product2.get_absolute_url()
        self.assertNotEqual(url2, absolute_url)
        self.assertTrue(url2.find(absolute_url[:1]) != -1)


class ProductImageTestCase(TestCase):

    def test___str__(self):
        image_not_main = ProductImage.objects.create(is_main=False)
        id = image_not_main.id
        self.assertEqual(str(id), str(image_not_main))




