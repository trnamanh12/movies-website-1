from django.urls import path
from . import views

urlpatterns = [
    # Movie-related URLs
    path('', views.movie_list, name='movie_list'),  # Display a list of all movies
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),  # Display details for a specific movie
    path('movies/<int:movie_id>/review/', views.add_review, name='add_review'),  # Add a review for a specific movie
    
    # Cinema-related URLs
    path('cinemas/', views.cinema_list, name='cinema_list'),  # Display a list of all cinemas
    path('cinemas/<int:cinema_id>/', views.cinema_detail, name='cinema_detail'),  # Display details for a specific cinema
    
    # Ticket booking URLs
    path('screenings/<int:screening_id>/book/', views.book_ticket, name='book_ticket'),  # Book a ticket for a specific screening
    # path('booking-confirmation/<int:ticket_id>/', views.booking_confirmation, name='booking_confirmation'),  # Display booking confirmation for a specific ticket

    path('search/', views.search, name='search'),  # Search for movies and cinemas

    path('save_movie/<int:movie_id>/', views.save_movie, name='save_movie'),  # Save a movie to the user's watchlist
    path('viewing_history/', views.viewing_history, name='viewing_history'),  # Display the user's viewing history
    path('view_saved_movies/', views.view_saved_movies, name='view_saved_movies'),  # Display the user's saved movies
]
