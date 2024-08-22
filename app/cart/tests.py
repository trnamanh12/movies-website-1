from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Cart, CartItem, Payment
from movies.models import Ticket, Screening, Cinema, Movie, TicketType
from django.utils import timezone

class CartViewsTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user(username='testuser', password='testpassword')
		self.screening = Screening.objects.create(movie=Movie.objects.create(title='Test Movie'), cinema=Cinema.objects.create(name='Test Cinema'), date_time=timezone.now())
		self.ticket_type = TicketType.objects.create(name='Test Ticket Type', price=10)
		self.ticket = Ticket.objects.create(screening=self.screening, ticket_type=self.ticket_type, user=self.user)
		self.cart = Cart.objects.create(user=self.user)
		self.cart_item = CartItem.objects.create(cart=self.cart, ticket=self.ticket, quantity=1)
		self.client.login(username='testuser', password='testpassword')

	def test_add_to_cart(self):
		response = self.client.post(reverse('add_to_cart', args=[self.ticket.id]))
		self.assertEqual(response.status_code, 302)
		self.assertTrue(CartItem.objects.filter(cart=self.cart, ticket=self.ticket).exists())

	def test_view_cart(self):
		response = self.client.get(reverse('view_cart'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'cart/view_cart.html')
		self.assertContains(response, self.cart_item.ticket)

	def test_remove_from_cart(self):
		response = self.client.post(reverse('remove_from_cart', args=[self.cart_item.id]))
		self.assertEqual(response.status_code, 302)
		self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())

	def test_checkout(self):
		response = self.client.post(reverse('checkout'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'cart/checkout_success.html')
		# self.assertEqual(Payment.objects.filter(user=self.user, status='Completed').count(), 1)
		# self.assertEqual(CartItem.objects.filter(cart=self.cart).count(), 0)

