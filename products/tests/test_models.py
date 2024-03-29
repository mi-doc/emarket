import os

from django.test import TestCase
from mixer.backend.django import mixer

from ..models import Product, ProductImage


class ProductTestCase(TestCase):

    def setUp(self):
        product = mixer.blend(Product, price=10000, discount=10, name='Samsung')
        product.save()

    def test_get_price_with_discount(self):
        product = mixer.blend(Product, price=10000, discount=10)
        product.save()
        discounted_price = int(product.get_price_with_discount())
        self.assertEqual(discounted_price, 9000)

        product = mixer.blend(Product, price=25000, discount=8)
        product.save()
        discounted_price = int(product.get_price_with_discount())
        self.assertEqual(discounted_price, 23000)

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

    def test_set_main_img(self):
        product = Product.objects.first()
        first_image = mixer.blend(ProductImage, product=product, is_main=True)
        second_image = mixer.blend(ProductImage, product=product, is_main=False)

        self.assertEqual(
            product.get_main_img_url(),
            first_image.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            second_image.image.url
        )

        product.set_main_img(main_img_id=second_image.id)

        self.assertEqual(
            product.get_main_img_url(),
            second_image.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            first_image.image.url
        )

        product.set_main_img()
        # Without keyword argument main_img_id nothing should happen

        self.assertEqual(
            product.get_main_img_url(),
            second_image.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            first_image.image.url
        )

        product.set_main_img(main_img_id=123123123123123)
        # With wrong id nothing should happen

        self.assertEqual(
            product.get_main_img_url(),
            second_image.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            first_image.image.url
        )

    def test_get_main_image_url_without_main_image(self):
        product = Product.objects.first()
        image_not_main1 = mixer.blend(ProductImage, product=product, is_main=False)
        image_not_main2 = mixer.blend(ProductImage, product=product, is_main=False)

        self.assertEqual(
            # Because the product model automatically makes the first image as main, if not specified.
            product.get_main_img_url(),
            image_not_main1.image.url
        )
        self.assertNotEqual(
            product.get_main_img_url(),
            image_not_main2.image.url
        )

    def test_get_main_image_url_without_images(self):
        product = Product.objects.first()
        self.assertEqual(
            product.get_main_img_url(),
            None
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

    def test_get_field_choices(self):
        product = mixer.blend(Product, price=25000, name='meizu mx5', os='android')
        product.save()
        product2 = mixer.blend(Product, os='android', name='whatever')
        product2.save()
        product3 = mixer.blend(Product, os='ios', name='iphone')
        product3.save()
        
        res = Product.objects.get_field_choices('os')
        self.assertEqual(len(res), 2)
        self.assertIn(('android', 'android'), res)
        self.assertIn(('ios', 'ios'), res)
    
    def test_get_max_and_min_specs(self):
        p1 = mixer.blend(Product, price=12000, built_in_memory=64, name='Samsung Galaxy')
        p1.save()
        p2 = mixer.blend(Product, price=15000, built_in_memory=128, name='Samsung Ultra')
        p2.save()
        p3 = mixer.blend(Product, price=9000, built_in_memory=64, name='Xiaomi')
        p3.save()
        p4 = mixer.blend(Product, price=22000, built_in_memory=256, name='Sony')
        p4.save()

        self.assertEqual(Product.objects.get_max_price(), p4.price)
        self.assertEqual(Product.objects.get_min_price(), p3.price)
        self.assertEqual(Product.objects.get_min_memory(), p1.built_in_memory)
        self.assertEqual(Product.objects.get_max_memory(), p4.built_in_memory)


class ProductImageTestCase(TestCase):

    def test___str__(self):
        image_not_main = ProductImage.objects.create(is_main=False)
        id = image_not_main.id
        self.assertEqual(str(id), str(image_not_main))
