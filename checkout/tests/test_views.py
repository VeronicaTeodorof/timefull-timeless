from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from gallery.models import Sculpture, Theme
from checkout.models import DeliveryCost, Order, OrderLineItem
from pages.models import BusinessSettings

User = get_user_model()


class CreateCheckoutSessionTests(TestCase):
    """
    Tests for the create_checkout_session view
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testbuyer',
            email='buyer@example.com',
            password='testpass'
        )
        self.client.login(username='testbuyer', password='testpass')

        self.theme = Theme.objects.create(name='Test Theme')

        self.sculpture = Sculpture.objects.create(
            title='Test Sculpture',
            material='Bronze',
            price=Decimal('100.00'),
            year=2025,
            image='image/upload/v1/original.jpg',
        )
        self.sculpture.themes.add(self.theme)

        DeliveryCost.objects.create(country='UK', cost=Decimal('40.00'))
        DeliveryCost.objects.create(country='RO', cost=Decimal('15.00'))

        self.business_settings = BusinessSettings.load()

    def test_create_checkout_session_blocks_sold_sculpture(self):
        """
        Tests that create_checkout_session redirects away and does not
        create a Stripe session when POST is sent directly for an already sold
        sculpture, without going through the terms page.
        """
        self.sculpture.status = 'sold'
        self.sculpture.save()

        response = self.client.post(
            reverse('checkout:create_checkout_session',
                    args=[self.sculpture.slug]),
            {'shipping_method': 'pickup'}
        )

        self.assertRedirects(response, reverse('gallery:sculpture-detail',
                                               args=[self.sculpture.slug]))


class StripeWebhookTests(TestCase):

    # Written adapting this resource:
    # https://dev.to/aakas/webhooks-in-django-a-comprehensive-guide-44jp
    # with help from Claude AI
    def test_webhook_rejects_invalid_signature(self):
        """
        Tests that stripe_webhook returns 400 when the Stripe-Signature
        header is invalid, rather than processing the event.
        """
        payload = '{"id": "evt_test", "type": "checkout.session.completed"}'

        response = self.client.post(
            reverse('checkout:payment-webhook'),
            data=payload,
            content_type='application/json',
            HTTP_STRIPE_SIGNATURE='invalid_signature'
        )
        self.assertEqual(response.status_code, 400)


class OrderHistoryViewTests(TestCase):
    """Tests for the order history view."""

    def setUp(self):
        """
        Creates temporary test data
        """
        self.user = User.objects.create_user(
            username="buyer1", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="buyer2", password="testpass123"
        )

        self.theme = Theme.objects.create(name='Test Theme')

        self.sculpture = Sculpture.objects.create(
            title='Test Sculpture',
            material='Bronze',
            price=Decimal('100.00'),
            year=2025,
            image='image/upload/v1/original.jpg',
        )
        self.sculpture.themes.add(self.theme)

        self.own_order = Order.objects.create(
            user=self.user,
            full_name="Buyer One",
            email="buyer1@example.com",
            country="UK",
            shipping_method="pickup",
            stripe_pid="pid_123",
        )
        OrderLineItem.objects.create(
            order=self.own_order,
            sculpture=self.sculpture,
            price_at_purchase=500,
            insurance_cost=7.50,
        )

        self.other_order = Order.objects.create(
            user=self.other_user,
            full_name="Buyer Two",
            email="buyer2@example.com",
            country="UK",
            shipping_method="pickup",
            stripe_pid="pid_456",
        )
        OrderLineItem.objects.create(
            order=self.other_order,
            sculpture=self.sculpture,
            price_at_purchase=500,
            insurance_cost=7.50,
        )

    def test_anonymous_user_redirected_to_login(self):
        """
        Tests that an anonymous request is redirected (not shown order data)
        """
        response = self.client.get(reverse("checkout:order_history"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_sees_own_order(self):
        """
        Tests that a logged-in user's own order appears in their history
        """
        self.client.login(username="buyer1", password="testpass123")
        response = self.client.get(reverse("checkout:order_history"))
        self.assertContains(response, self.own_order.order_number)

    def test_authenticated_user_does_not_see_others_orders(self):
        """
        Tests that a logged-in user cannot see another user's order
        """
        self.client.login(username="buyer1", password="testpass123")
        response = self.client.get(reverse("checkout:order_history"))
        self.assertNotContains(response, self.other_order.order_number)
