from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from checkout.models import Order, OrderLineItem
from gallery.models import Sculpture, Theme
from django.db import models


User = get_user_model()


class OrderModelTests(TestCase):

    def setUp(self):
        """
        Creates a temporary User for tests
        """
        self.user = User.objects.create_user(
            username='testbuyer',
            email='buyer@example.com',
            password='testpass123'
        )

    def test_order_number_field_exists_and_is_not_editable(self):
        """
        Tests that order_number exists as a field and is marked
        non-editable, since it should never be user-entered.
        """
        field = Order._meta.get_field('order_number')
        self.assertEqual(field.max_length, 32)
        self.assertFalse(field.editable)

    def test_shipping_method_field_choices(self):
        """
        Tests that shipping_method offers exactly the two expected
        choices: delivery and pickup.
        """
        field = Order._meta.get_field('shipping_method')
        choice_values = [choice[0] for choice in field.choices]
        self.assertIn('delivery', choice_values)
        self.assertIn('pickup', choice_values)

    def test_postcode_is_nullable(self):
        """
        Tests that an Order can be created with
        postcode=None, since null=True.
        """
        try:
            Order.objects.create(
                user=self.user,
                full_name='Test Buyer',
                email='buyer@example.com',
                phone_number='07123456789',
                country='UK',
                town_or_city='London',
                street_address1='123 Test Street',
                shipping_method='pickup',
                stripe_pid='pi_test456',
                postcode=None,
            )
        except IntegrityError:
            self.fail("postcode should allow null=True")

    def test_shipped_at_is_nullable(self):
        """
        Tests that an Order can be created with
        shipped_at=None, since null=True.
        """
        try:
            Order.objects.create(
                user=self.user,
                full_name='Test Buyer',
                email='buyer@example.com',
                phone_number='07123456789',
                country='UK',
                town_or_city='London',
                street_address1='123 Test Street',
                shipping_method='pickup',
                stripe_pid='pi_testdef',
                shipped_at=None,
            )
        except IntegrityError:
            self.fail("shipped_at should allow null=True")

    def test_order_number_auto_generates_on_save(self):
        """
        Tests that a new Order is given an order_number automatically
        on save
        """
        order = Order.objects.create(
            user=self.user,
            full_name='Test Buyer',
            email='buyer@example.com',
            phone_number='07123456789',
            country='UK',
            town_or_city='London',
            street_address1='123 Test Street',
            shipping_method='pickup',
            stripe_pid='pi_test999',
        )
        self.assertTrue(order.order_number)


class OrderLineItemRawModelTests(TestCase):

    def setUp(self):
        """
        Creates a temporary User, Order, Theme, and Sculpture for tests
        """
        self.user = User.objects.create_user(
            username='testbuyer',
            email='buyer@example.com',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test Buyer',
            email='buyer@example.com',
            phone_number='07123456789',
            country='UK',
            town_or_city='London',
            street_address1='123 Test Street',
            shipping_method='pickup',
            stripe_pid='pi_test123',
        )
        self.theme = Theme.objects.create(name='Test Theme')
        self.sculpture = Sculpture.objects.create(
            title='Test Sculpture',
            year=2024,
            price=100.00,
            image='image/upload/v1234/test_sculpture.jpg',
            material='Bronze',
        )
        self.sculpture.themes.add(self.theme)

    def test_orderlineitem_has_order_field(self):
        """
        Tests that order is a ForeignKey on OrderLineItem model
        """
        field = OrderLineItem._meta.get_field('order')
        self.assertIsInstance(field, models.ForeignKey)

    def test_orderlineitem_has_sculpture_field(self):
        """
        Tests that sculpture is a ForeignKey on OrderLineItem model
        """
        field = OrderLineItem._meta.get_field('sculpture')
        self.assertIsInstance(field, models.ForeignKey)

    def test_orderlineitem_delivery_cost_defaults_to_zero(self):
        """
        Tests that delivery_cost defaults to 0, since Studio Pickup
        orders have no delivery cost.
        """
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            sculpture=self.sculpture,
            price_at_purchase=100.00,
            insurance_cost=1.50,
        )
        self.assertEqual(lineitem.delivery_cost, 0)

    def test_orderlineitem_total_field_is_not_editable(self):
        """
        Tests that lineitem_total is marked non-editable, since it
        should always be calculated, never user-entered.
        """
        field = OrderLineItem._meta.get_field('lineitem_total')
        self.assertFalse(field.editable)
