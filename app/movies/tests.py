from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Movie, Cinema, Screening, TicketType, Ticket, Review
from django.utils import timezone
from cart.models import Cart, CartItem, Payment

class MovieViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.movie = Movie.objects.create(title='Test Movie', vote_average=8.5)
        self.movie_for_test_booking = Movie.objects.create(title='Test Movie 1', vote_average=8.5)

        self.cinema = Cinema.objects.create(name='Test Cinema', address='Test Address')
        self.cinema_for_test_booking = Cinema.objects.create(name='Test Cinema 1', address='Test Address 1')

        self.screening = Screening.objects.create(movie=self.movie, cinema=self.cinema, date_time=timezone.now())
        self.ticket_type = TicketType.objects.create(name='Test Ticket Type', price=10)
        self.ticket = Ticket.objects.create(screening=self.screening, ticket_type=self.ticket_type, user=self.user)
        self.screening_for_test_booking = Screening.objects.create(movie=self.movie_for_test_booking, cinema=self.cinema_for_test_booking, date_time=timezone.now())
        self.client.login(username='testuser', password='testpassword')

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/home.html')

    def test_movie_list_view(self):
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_list.html')
        self.assertContains(response, self.movie.title)

    def test_movie_detail_view(self):
        response = self.client.get(reverse('movie_detail', args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_detail.html')
        self.assertContains(response, self.movie.title)

    def test_add_review_view(self):
        response = self.client.post(reverse('add_review', args=[self.movie.id]), {
            'rating': 5,
            'comment': 'Great movie!'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful review submission
        self.assertTrue(Review.objects.filter(movie=self.movie, user=self.user).exists())

    def test_cinema_list_view(self):
        response = self.client.get(reverse('cinema_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/cinema_list.html')
        self.assertContains(response, self.cinema.name)

    def test_cinema_detail_view(self):
        response = self.client.get(reverse('cinema_detail', args=[self.cinema.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/cinema_detail.html')
        self.assertContains(response, self.cinema.name)

    def test_book_ticket_view(self):
        response = self.client.post(reverse('book_ticket', args=[self.screening_for_test_booking.id]), {
            'ticket_type': self.ticket_type.id,
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Ticket.objects.filter(screening=self.screening_for_test_booking, user=self.user).exists())
        ticket = Ticket.objects.get(screening=self.screening_for_test_booking, user=self.user)
        self.assertTrue(CartItem.objects.filter(ticket=ticket).exists())

    def test_search_view(self):
        response = self.client.get(reverse('search'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/search_results.html')
        self.assertContains(response, self.movie.title)
        self.assertContains(response, self.cinema.name)