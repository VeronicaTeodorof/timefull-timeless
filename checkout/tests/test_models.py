from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from checkout.models import Order

User = get_user_model()


class OrderRawModelTests(TestCase):

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
