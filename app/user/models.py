from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

#     def __str__(self):
#         return f'{self.user.username} - Balance: {self.balance}'

#     def getBalance(self):
#         return self.balance
    