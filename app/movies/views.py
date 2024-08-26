from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from movies.models import Movie, Cinema, Screening, TicketType, Ticket, Review, UserHistory
from django.http import HttpResponse, HttpRequest
from .forms import ReviewForm, TicketForm
from random import sample
from cart.views import add_to_cart
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .utilss import semantic_search


def home(request : 'HttpRequest') -> 'HttpResponse':
    # Get top 100 movies with the highest vote_average
    top_movies = Movie.objects.order_by('-vote_average')[:1000]

    # Get random movies from top 100 movies
    top_movies = sample(list(top_movies), min(len(top_movies), 18))
    base_image_url = 'https://image.tmdb.org/t/p/w500'

    # Get all cinemas and select 10 random ones
    all_cinemas = list(Cinema.objects.all())
    random_cinemas = sample(all_cinemas, min(len(all_cinemas), 10))
    
    return render(request, 'movies/home.html', {
        'featured_movies': top_movies,
        'top_cinemas': random_cinemas,
        'base_image_url': base_image_url,
    })


def movie_list(request: 'HttpRequest') -> 'HttpResponse':
    query = request.GET.get('q')  # Get the query string from the URL
    if query:
        movies = Movie.objects.filter(title__icontains=query)
    else:
        movies = Movie.objects.all()
    
    paginator = Paginator(movies, 12)  # Show 12 movies per page
    page = request.GET.get('page')
    
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'base_image_url': base_image_url,
        'query': query,
        'paginator': paginator,
    })

def movie_detail(request: 'HttpRequest', movie_id: int) -> 'HttpResponse':
    movie = get_object_or_404(Movie, id=movie_id)
    
    # Record the user's history
    if request.user.is_authenticated:
        record_movie_history(request, movie)
    
    screenings = movie.screenings.select_related('cinema').order_by('date_time')
    reviews = movie.reviews.select_related('user').order_by('-created_at') # order by newest first
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    recommended_movies = movie.get_recommendations()
    return render(request, 'movies/movie_detail.html', {
        'movie': movie,
        'screenings': screenings,
        'reviews': reviews,
        'base_image_url': base_image_url,
        'recommended_movies': recommended_movies,
    })

@login_required
def add_review(request: 'HttpRequest', movie_id: int) -> 'HttpResponse':
    movie = get_object_or_404(Movie, id=movie_id)
    existing_review = Review.objects.filter(movie=movie, user=request.user).first()
    # existing_review return None if no review exists
    
    if existing_review:
        messages.error(request, "You have already submitted a review for this movie.")
        return redirect('movie_detail', movie_id=movie_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Review added successfully.")
            return redirect('movie_detail', movie_id=movie_id)
        else:
            messages.error(request, "There was an error in your submission. Please correct the highlighted fields.")

    else:
        form = ReviewForm()

    return render(request, 'movies/add_review.html', {'form': form, 'movie': movie})

def cinema_list(request: 'HttpRequest') -> 'HttpResponse':
    cinemas = Cinema.objects.all()
    return render(request, 'movies/cinema_list.html', {'cinemas': cinemas})

def cinema_detail(request: 'HttpRequest', cinema_id: int) -> 'HttpResponse':
    # can add image_url to the context to display cinema image
    cinema = get_object_or_404(Cinema, id=cinema_id)
    screenings = cinema.screenings.select_related('movie').order_by('date_time')
    return render(request, 'movies/cinema_detail.html', {'cinema': cinema, 'screenings': screenings})

@login_required
def book_ticket(request: 'HttpRequest', screening_id: int) -> 'HttpResponse':
    screening = get_object_or_404(Screening, id=screening_id)
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.screening = screening
            ticket.user = request.user
            ticket.save()
            # messages.success(request, "Ticket booked successfully.")
            # return redirect('add_to_cart', ticket.id)
            add_to_cart(request, ticket.id)  # Add ticket to cart
            return redirect( 'booking_confirmation', ticket.id)
        else:
            messages.error(request, "There was an error in your submission. Please correct the highlighted fields.")
    else:
        form = TicketForm()

    return render(request, 'movies/book_ticket.html', {
        'form': form,
        'screening': screening,
    })

@login_required
def booking_confirmation(request: 'HttpRequest', ticket_id: int) -> 'HttpResponse':
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    return render(request, 'movies/booking_confirmation.html', {'ticket': ticket})

def search(request: 'HttpRequest') -> 'HttpResponse':
    query = request.GET.get('q')
    movies = Movie.objects.filter(title__icontains=query)
    cinemas = Cinema.objects.filter(name__icontains=query)
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    return render(request, 'movies/search_results.html', {'movies': movies, 'cinemas': cinemas, 'base_image_url': base_image_url})

def semantic_search_view(request: 'HttpRequest') -> 'HttpResponse':
    if request.method == 'GET':
        query = request.GET.get('q')
        results = semantic_search(query)
        movies = Movie.objects.filter(title__in=results)
        movie_base_url = 'https://image.tmdb.org/t/p/w500'
    return render(request, 'movies/semantic_search_results.html', {'movies': movies, 'base_image_url': movie_base_url})

@login_required
def save_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        _ , _ = UserHistory.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={'saved': True}
        )
    messages.success(request, "Movie saved successfully.")
    return redirect('movie_detail', movie_id=movie_id)


@login_required
def record_movie_history(request, movie):
    UserHistory.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={'last_watched': timezone.now()}
    )

@login_required
def viewing_history(request):
    user_histories = UserHistory.objects.filter(user=request.user).order_by('-last_watched')
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    return render(request, 'movies/viewing_history.html', {'user_histories': user_histories, 'base_image_url': base_image_url})

@login_required
def view_saved_movies(request):
    saved_movies = UserHistory.objects.filter(user=request.user, saved=True)
    base_image_url = 'https://image.tmdb.org/t/p/w500'
    return render(request, 'movies/view_saved_movies.html', {'saved_movies': saved_movies, 'base_image_url': base_image_url})

@login_required
def rating_history(request):
    user_reviews = Review.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'movies/rating_history.html', {'user_reviews': user_reviews})
