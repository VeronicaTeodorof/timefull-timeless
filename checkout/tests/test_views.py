from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from gallery.models import Sculpture, Theme
from checkout.models import DeliveryCost
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
