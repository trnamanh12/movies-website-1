from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from typing import List, Tuple

class Movie(models.Model):
    title = models.CharField(max_length=200)
    vote_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    vote_count = models.IntegerField(default=0)
    # price = models.DecimalField(max_digits=6, decimal_places=2)
    release_date = models.DateField(default='2020-01-01')
    revenue = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    overview = models.TextField(default='')
    image = models.URLField(max_length=200, default='')
    genres = models.CharField(max_length=200, default='')
    keywords = models.CharField(max_length=200, default='')

    
    def __str__(self) -> str:
        return self.title

    def find_index(self, name: str, movie2idx: pd.Series) -> int:
        return movie2idx.get(name, -1) # return -1 if not found

    def load_model_and_data(self) -> Tuple[pd.DataFrame, TfidfVectorizer, pd.Series]:
        try:
            idx_title = pd.read_csv('./data/indexed_movies.csv', index_col=0)
            with open('./model_rm/tfidf.pkl', 'rb') as f:
                tfidf = pickle.load(f)
            movie2idx = pd.Series(idx_title.index, index=idx_title['title'])
            return idx_title, tfidf, movie2idx
        except Exception as e:
            print(f"Error loading model and data: {e}")
            return pd.DataFrame(), None, pd.Series()

    def get_recommendations(self) -> List['Movie']:
        list_movies = []
        data, model, movie2idx = self.load_model_and_data()
        if model is None or data.empty:
            return list_movies

        idx = self.find_index(self.title, movie2idx)
        if idx == -1:
            return list_movies

        if isinstance(idx, pd.Series):
            idx = idx.iloc[0]

        try:
            result = (-(cosine_similarity(model[idx], model).flatten())).argsort()[1:10]
            result_titles = data['title'].iloc[result].tolist()
            for title in result_titles:
                movie = Movie.objects.filter(title=title).first()
                if movie:
                    list_movies.append(movie)
        except Exception as e:
            print(f"Error getting recommendations: {e}")

        return list_movies



class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews') 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return f"{self.user.username}'s review for {self.movie.title}"
    
    def get_rating(self):
        return '⭐' * self.rating

    def get_comment(self):
        return self.comment[:100] + ('...' if len(self.comment) > 100 else '')
    
    class Meta:
        unique_together = ('movie', 'user')

class Cinema(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    
    def __str__(self):
        return self.name

class Screening(models.Model):
    """
    table to store movie screenings:
    - movie: FK to Movie
    - cinema: FK to Cinema
    - date_time: datetime of the screening
    - time: time of the screening
    should I change this to many-to-many?
    because there are many cinemas and many movies each screening can be in multiple cinemas
    """
    # id = models.AutoField(primary_key=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='screenings')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, related_name='screenings')
    date_time = models.DateTimeField()
    
    def __str__(self):
        return f"{self.movie.title} at {self.cinema.name} - {self.date_time}"

class TicketType(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"Type: {self.name} - ${self.price}"

class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE, related_name='tickets')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, editable=False)

    def __str__(self):
        return f"{self.quantity} {self.ticket_type.name} for {self.screening}"
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.ticket_type.price
        super().save(*args, **kwargs)


# class Seen(models.Model):
#     """
#     table to store movies that user has seen
#     """
#     username = models.CharField(max_length=150)
#     movieid = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.username + '|' + self.movieid.movieid

# class Expect(models.Model):
#     """
#     table to store movies that user expects to see
#     """
#     username = models.CharField(max_length=150)
#     movieid = models.ForeignKey(Movie, default=1, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.username + '|' + self.movieid.movieid