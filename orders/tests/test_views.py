from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core import mail
from django.conf import settings
from django.urls import reverse
from mixer.backend.django import mixer
import json

from ..models import Order, Status, ProductInOrder, ProductInBasket
from accounts.models import Profile
from products.models import Product

User = get_user_model()

class UpdateBasketListViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='somep')
        self.user2 = User.objects.create_user(username='testuser2', password='somep')

        self.pr1 = mixer.blend(Product, price=12000)
        self.pr2 = mixer.blend(Product, price=13300)
        self.pr3 = mixer.blend(Product, price=14600)

        # self.order1 = mixer.blend(Order, user=self.user1)
        # self.order2 = mixer.blend(Order, user=self.user2)

        self.pr_in_basket1 = mixer.blend(
            ProductInBasket,
            user = self.user1,
            product = self.pr1,
            # order = self.order1
        )
        self.pr_in_basket2 = mixer.blend(
            ProductInBasket,
            user=self.user1,
            product=self.pr2,
        )
        self.pr_in_basket3 = mixer.blend(
            ProductInBasket,
            user=self.user2,
            product=self.pr2,
                )


    def test_view_url_exists_and_accessible(self):
        response = self.client.get('/orders/update_basket_list/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emarket/basket_items_list.html')

    def test_view_context_keys(self):
        response = self.client.get(reverse('orders:basket_list'))
        expected_context_keys = [
            'products_total_nmb',
            'products_in_basket_ids',
            'products_in_basket',
            'products_total_price'
        ]

        for key in expected_context_keys:
            self.assertIn(key, response.context)

    def test_view_context_with_user(self):

        # ::::First user::::
        self.client.login(username='testuser1', password='somep')

        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['products_total_nmb'], 2)

        ids = str(self.pr_in_basket1.product.id) + ',' + str(self.pr_in_basket2.product.id)
        self.assertEqual(response.context['products_in_basket_ids'], ids)

        total_price = self.pr_in_basket1.total_price + self.pr_in_basket2.total_price
        self.assertEqual(response.context['products_total_price'], total_price)

        # ::::And logout::::
        self.client.logout()
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.context['products_total_nmb'], 0)
        self.assertEqual(response.context['products_in_basket_ids'], '')
        self.assertEqual(response.context['products_total_price'], 0)

        # ::::And another user::::
        self.client.login(username='testuser2', password='somep')
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.context['products_total_nmb'], 1)

        ids = str(self.pr_in_basket3.product.id)
        self.assertEqual(response.context['products_in_basket_ids'], ids)

        total_price = self.pr_in_basket3.total_price
        self.assertEqual(response.context['products_total_price'], total_price)

    def test_add_product_to_basket_with_login(self):
        self.client.login(username='testuser1', password='somep')
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)

        pr_id = self.pr3.id
        response= self.client.post(reverse('orders:basket_list'), data={'product_id': pr_id, 'nmb': 3})
        self.assertEqual(response.context['products_total_nmb'], 3)

        ids = str(self.pr_in_basket1.product.id) + ',' + str(self.pr_in_basket2.product.id) + ','
        ids += str(pr_id)
        self.assertEqual(response.context['products_in_basket_ids'], ids)

        total_price = self.pr_in_basket1.total_price \
                      + self.pr_in_basket2.total_price \
                      + self.pr3.price * 3
        self.assertEqual(response.context['products_total_price'], total_price)

    def test_add_and_remove_product_from_basket_without_login(self):
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)

        pr_id = self.pr3.id
        pr2_id = self.pr2.id
        response = self.client.post(reverse('orders:basket_list'), data={'product_id': pr_id})
        response = self.client.post(reverse('orders:basket_list'), data={'product_id': pr2_id})
        self.assertEqual(response.context['products_total_nmb'], 2)


        response= self.client.post(reverse('orders:basket_list'), data={'remove_product_id': pr_id})
        self.assertEqual(response.context['products_total_nmb'], 1)

    def test_update_product_in_basket(self):
        self.client.login(username='testuser1', password='somep')
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.context['products_total_nmb'], 2)

        pr_id = self.pr1.id
        nmb1 = ProductInBasket.objects.get(user=self.user1, product_id=pr_id).nmb
        response = self.client.post(reverse('orders:basket_list'), data={'product_id': pr_id, 'nmb': 3})
        nmb2 = ProductInBasket.objects.get(user=self.user1, product_id=pr_id).nmb
        self.assertEqual(nmb2, nmb1 + 3)

    def test_delete_product_from_basket(self):
        self.client.login(username='testuser1', password='somep')
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)

        pr_id = self.pr_in_basket1.id
        response = self.client.post(reverse('orders:basket_list'), data={'remove_product_id': pr_id})
        self.assertEqual(response.context['products_total_nmb'], 1)

        ids = str(self.pr_in_basket2.product.id)
        self.assertEqual(response.context['products_in_basket_ids'], ids)

    def test_view_without_user(self):
        response = self.client.get(reverse('orders:basket_list'))
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['products_total_nmb'], 0)
        self.assertEqual(response.context['products_in_basket_ids'], '')
        self.assertEqual(response.context['products_total_price'], 0)

        pr3_id = self.pr3.id
        response = self.client.post(reverse('orders:basket_list'), data={'product_id': pr3_id, 'nmb': 2})
        self.assertEqual(response.context['products_total_nmb'], 1)
        self.assertEqual(response.context['products_in_basket_ids'], str(pr3_id))
        self.assertEqual(response.context['products_total_price'], self.pr3.price * 2)

        pr1_id = self.pr1.id
        response = self.client.post(reverse('orders:basket_list'), data={'product_id': pr1_id, 'nmb': 1})
        self.assertEqual(response.context['products_total_nmb'], 2)
        ids = str(pr3_id) + ',' + str(pr1_id)
        self.assertEqual(response.context['products_in_basket_ids'], ids)
        price = self.pr3.price * 2 + self.pr1.price
        self.assertEqual(response.context['products_total_price'], price)


class ChangeProductInBasketViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username='testuser1', password='somep')
        self.pr1 = mixer.blend(Product, price=12000)
        self.pr_in_basket1 = mixer.blend(
            ProductInBasket,
            user = self.user1,
            product = self.pr1,
        )

    def test_change_product_in_basket_nmb(self):
        data = {'product_id': self.pr1.id, 'nmb': 11}

        self.client.login(username='testuser1', password='somep')
        response = self.client.post(reverse('orders:changeProductQuantity'), data=data)

        self.assertEqual(response.status_code, 200)
        product = ProductInBasket.objects.filter(user=self.user1, product=self.pr1).first()
        self.assertEqual(product.nmb, 11)

class CheckoutViewTestCase(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='somep',
            email='test@testmail.com'
        )
        self.pr1 = mixer.blend(Product, name='Huawei 999')
        self.pr2 = mixer.blend(Product, name='New Iphone')

        self.pr_in_basket1 = mixer.blend(
            ProductInBasket,
            user=self.user1,
            product=self.pr1,
            # order = self.order1
        )
        self.pr_in_basket2 = mixer.blend(
            ProductInBasket,
            user=self.user1,
            product=self.pr2,
        )

    def test_view_url_exists_and_accessible(self):
        response = self.client.get('/orders/checkout/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/checkout.html')

    def test_view_context_keys(self):
        response = self.client.get(reverse('orders:checkout'))
        expected_context_keys = [
            'products_in_basket',
            'products_total_price',
            'form'
        ]

        for key in expected_context_keys:
            self.assertIn(key, response.context)

    def test_view_with_valid_data(self):
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ProductInOrder.objects.count(), 0)

        data = {
            'customer_name': 'tester',
            'customer_phone': 11112232,
            'customer_email': 'test@test.com',
            'customer_address': 'Moskva, Liteynaya',
            'comments': 'I am ok'
        }
        self.client.login(username='testuser1', password='somep')
        response = self.client.post(reverse('orders:checkout'), data)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(ProductInOrder.objects.count(), 2)
        self.assertEqual(Order.objects.first().comments, 'I am ok')
        self.assertEqual(Order.objects.first().user, self.user1)
        self.assertTemplateNotUsed(response, 'orders/checkout.html')
        self.assertRedirects(response, reverse('orders:success'))

        # Email notifications to ADMINS
        self.assertEqual(len(mail.outbox), 1)
        msg = mail.outbox[0]
        for admin in settings.ADMINS:
            self.assertIn(admin[1], msg.recipients())

        msg_text = msg.body
        for val in data.values():
            self.assertIn(str(val), msg_text)
        self.assertIn(self.pr1.name, msg_text)
        self.assertIn(self.pr2.name, msg_text)


    def test_view_with_valid_data_and_anonimous_user(self):
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ProductInOrder.objects.count(), 0)

        data = {
            'customer_name': 'tester',
            'customer_phone': 11112232,
            'customer_email': 'test@test.com',
            'customer_address': 'Moskva, Liteynaya',
            'comments': 'I am ok'
        }
        response = self.client.post(reverse('orders:checkout'), data)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(ProductInOrder.objects.count(), 0)
        self.assertEqual(Order.objects.first().customer_name, 'tester')
        self.assertIsNone(Order.objects.first().user)
        self.assertTemplateNotUsed(response, 'orders/checkout.html')

    def test_view_with_invalid_data(self):
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ProductInOrder.objects.count(), 0)

        # Invalid phone
        data = {
            'name': 'tester',
            'phone': '',
            'email': 'test@test.com',
            'address': 'Moskva, Liteynaya',
            'comments': 'I am ok'
        }
        self.client.login(username='testuser1', password='somep')
        response = self.client.post(reverse('orders:checkout'), data)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ProductInOrder.objects.count(), 0)

        # Invalid email
        data = {
            'name': 'tester',
            'phone': 1231231231,
            'email': 'test@test',
            'address': 'Moskva, Liteynaya',
            'comments': 'I am ok'
        }
        self.client.login(username='testuser1', password='somep')
        response = self.client.post(reverse('orders:checkout'), data)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(ProductInOrder.objects.count(), 0)

    def test_prefill_form_data_with_user(self):
        profile = mixer.blend(
            Profile,
            user=self.user1,
            first_name=mixer.FAKE,
            second_name=mixer.FAKE,
            address=mixer.FAKE,
            phone=mixer.FAKE
        )

        self.client.login(username='testuser1', password='somep')
        response = self.client.get(reverse('orders:checkout'))
        self.assertEqual(response.context['form'].initial['customer_name'], profile.get_full_name())
        self.assertEqual(response.context['form'].initial['customer_address'], profile.address)
        self.assertEqual(response.context['form'].initial['customer_email'], self.user1.email)
        self.assertEqual(response.context['form'].initial['customer_phone'], profile.phone)


class SuccessViewTestCase(TestCase):

    def test_view_url_exists_and_accessible(self):
        response = self.client.get('/orders/success/')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('orders:success'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('orders:success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders/success.html')

    def test_view_context_keys_without_authentication(self):
        response = self.client.get(reverse('orders:success'))
        expected_context_key = 'user_profile_page'
        self.assertNotIn(expected_context_key, response.context)

    def test_view_context_keys_with_authentication(self):
        user = User.objects.create_user(
            username='testuser1',
            password='somep',
            email='test@testmail.com'
        )
        profile = mixer.blend(Profile, user=user)
        self.client.login(username='testuser1', password='somep')
        response = self.client.get(reverse('orders:success'))
        expected_context_key = 'user_profile_url'
        self.assertIn(expected_context_key, response.context)
        self.assertEqual(response.context['user_profile_url'], user.profile.get_absolute_url())
