# Cafeteria Management System API

This is the backend API for the Cafeteria Management System, built with Django and Django Rest Framework (DRF). The API supports functionalities such as user management, food item management, order processing, and more.

## Features

- User authentication and management
- Food categories and item management
- Order and review processing
- Dining table management
- Special offers and customer points system
- JWT authentication for securing API endpoints

## Installation

1. Clone the repository:


## API Endpoints

1. Authentication: 


Todo:
-Handle sending the orderitems when the order is created successfully.(Modify the OrderSerializer)
-Fetch notifications, mark read, mark all as read
- payment notifications , payment model
- Redeem points, create redemption options endpoints, fetch redemption options.a user redeems point for a fooditem, points decreased, new order created with is_paid status marked true, send notification to both user and admin
- admin processing paid orders update status of order, view all orders and filter by order status