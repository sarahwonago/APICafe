from .models import Order, CustomerPoint, Transaction, RedemptionTransaction


def calculate_points(total_price):
    """
    Calculates the total points earned based on the orders total price.
    User earns 1 point for every 100ksh spent.
    """

    return int(total_price/100)

def assign_points(order:Order):
    """
    Awards points to users and creates a transaction for it.
    """
    user = order.user
    total_price = order.total_price
    points = calculate_points(total_price=total_price)
    
    # gets or creates a customer_point object and assigns points
    customer_point, created = CustomerPoint.objects.get_or_create(user=user)
    customer_point.points += points
    customer_point.save()

    # creates a new transaction for the point assigned
    new_transaction = Transaction.objects.create(
        customer_point=customer_point,
        amount=total_price,
        points_earned=points
    )


def redeem_points(user,redemption_option):
    """
    Redeems customerpoints and creates a transaction for it.
    """ 

    user_points = user.customerpoints
    points_redeemed = redemption_option.points_required

    # if user points is >= to points required, a redemption transaction is created for the user
    if user_points.points >= points_redeemed:
        redemption_transaction = RedemptionTransaction.objects.create(
            customer=user,
            redemption_option=redemption_option,
            points_redeemed =  points_redeemed,
        )

        # reduce customer points
        user_points.points -= points_redeemed
        user_points.save()

        return redemption_transaction
    
    return None
    

    


