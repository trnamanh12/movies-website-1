from django.db import models
from django.contrib.auth.models import User
from movies.models import Ticket

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_amount(self):
        return sum(item.ticket.ticket_type.price * item.quantity for item in CartItem.objects.filter(cart=self))

    def __str__(self):
        return f"Cart of {self.user.username}"
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.ticket} in {self.cart}"
    
    @property
    def get_ticket_price(self):
        return self.ticket.ticket_type.price
    
    @property
    def get_quantity(self):
        return self.quantity

    @property
    def get_total_price(self):
        return self.get_ticket_price * self.get_quantity
    
    class Meta:
        unique_together = ('cart', 'ticket')

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    # amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment of {self.bill} by {self.user.username} - {self.status}"
    
    @property
    def bill(self):
        return self.cart.get_total_amount