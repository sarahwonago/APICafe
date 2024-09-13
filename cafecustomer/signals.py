from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem

@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    """
    Signal to update the cart's total price when CartItem is saved or deleted.
    """
    cart = instance.cart
    cart.save()  # Triggers the @property total_price to update