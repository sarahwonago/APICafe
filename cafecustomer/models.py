import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    """
    Model representing a category for food items.

    Attributes:
        id (UUIDField): The unique identifier for the category.
        name (CharField): The name of the category.
        description (TextField): A brief description of the category.
        created_at (DateTimeField): The timestamp when the category was created.
        updated_at (DateTimeField): The timestamp when the category was last updated.
    """

    class Meta:
        verbose_name_plural = "Categories"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    """
    Model representing a fooditem.

    Attributes:
        id (UUIDField): The unique identifier for the fooditem.
        category (ForeignKey): The category in which the fooditem belongs to.
        name (CharField): The name of the fooditem.
        price (DecimalField): The price of the fooditem.
        #image = models.ImageField(upload_to="food_images/", default="food_images/default.jpg")
        description (TextField): Brief description for the fooditem.
        created_at (DateTimeField): Timestamp when the fooditem was created.
        updated_at (DateTimeField): Timestamp when the fooditem was updated.
        is_available (BooleanField): Availability of the fooditem.

    """

    class Meta:
        verbose_name_plural = "FoodItems"
        

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        Category,
        related_name="fooditems",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    # image = models.ImageField(upload_to="food_images/", default="food_images/default.jpg")
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField("Availability", default=False)

    def __str__(self):
        return self.name


class DiningTable(models.Model):
    """
    Defines the dining tables.
    """

    class Meta:
        verbose_name_plural = "Dining Tables"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    table_number = models.PositiveIntegerField(verbose_name="Table Number", unique=True)
    is_occupied = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Table {self.table_number}"

class UserDinningTable(models.Model):
    """
    Defines categories for food items.
    """

    class Meta:
        verbose_name_plural = "User Dinning Tables"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User,
        related_name="userdinningtable",
        on_delete=models.CASCADE,
       
    )
    dinning_table = models.ForeignKey(DiningTable, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Dinning Table:{self.dinning_table.table_number}" if self.dinning_table else  f"{self.user.username} Dinning at:_" 


class Order(models.Model):
    """
    Defines the orders.
    """

    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-updated_at']

    
    ESTIMATED_TIME_CHOICES = [(i, f"{i} minutes") for i in range(5, 65, 5)]
    STATUS_CHOICES = (
        ("COMPLETE", "Complete"),
        ("PENDING", "Pending")
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        related_name="orders",
        on_delete=models.CASCADE
    )
    
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_paid = models.BooleanField(default=False)
    estimated_time = models.IntegerField(
        "Estimated Delivery Time",
        choices=ESTIMATED_TIME_CHOICES,
        default=5
    )
    status = models.CharField(max_length=250, default="PENDING", choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    


class OrderItem(models.Model):
    """
    Defines the individual items within an order.
    """

    class Meta:
        verbose_name_plural = "Order Items"
        unique_together = ('order', 'fooditem')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(
        Order,
        related_name="orderitems",
        on_delete=models.CASCADE
    )
    fooditem = models.ForeignKey(
        FoodItem,
        related_name="orderitems",
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(
        default = 1,
        validators=[MinValueValidator(1)],
        help_text="Quantity of the item"
    )

    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.fooditem.name} (Order {self.order.id})"


class Review(models.Model):
    """
    Defines the reviews for orders.
    """

    class Meta:
        verbose_name_plural = "Reviews"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        related_name="reviews",
        on_delete=models.CASCADE
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="review")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order {self.order.id}"


class CustomerPoint(models.Model):
    """
    Defines the customer points.
    """

    class Meta:
        verbose_name_plural = "CustomerPoints"
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customerpoints")
    points = models. PositiveIntegerField(default=0)

class Transaction(models.Model):
    """
    Defines when each customer point was awarded.
    """

    class Meta:
        verbose_name_plural = "Transaction"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_point = models.ForeignKey(CustomerPoint, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # order total 
    points_earned = models.PositiveIntegerField() # points awarded based on the order total
    date = models.DateTimeField(auto_now_add=True)


class SpecialOffer(models.Model):
    """
    Defines special offer.
    """

    class Meta:
        verbose_name_plural = "SpecialOffers"

    OFFER_CHOICES = (
        ('CHRISTMAS','Christmas'),
        ('BOXING DAY', 'Boxing Day'),
        ('EASTER', 'Easter')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, choices=OFFER_CHOICES)
    fooditem = models.ForeignKey(
        FoodItem,
        related_name="specialoffer",
        on_delete=models.CASCADE
    )
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)  # e.g., 20.00 for 20%
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.fooditem.name} - {self.discount_percentage}% Off"
    

class RedemptionOption(models.Model):
    name = models.CharField(max_length=100)
    points_required = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Redeem {self.name} for {self.points_required} points"
    

class RedemptionTransaction(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    redemption_option = models.ForeignKey(RedemptionOption, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.name} redeemed {self.redemption_option.points_required} points"