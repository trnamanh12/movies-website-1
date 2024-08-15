from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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

    
    def __str__(self):
        return self.title

    def get_recommendations(self):
        # return Movie.objects.exclude(id=self.id).order_by('-vote_average')[:5]
        pass

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