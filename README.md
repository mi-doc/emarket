# Emarket
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Functionality](#functionality)
* [Setup](#setup)

## General info
Minimalistic online tablet store. 
Provides the most basic functionality for customers and staff. 
This is a training project. 

Deployed version: http://emarket-store.ru 
(might not be available if server subscription has ended)

## Technologies
- Python 3.8
- Django 3.0
- Django Rest Framework
- Javascript, jquery
- HTML, css
- PostgreSQL
- Nginx
- Docker-compose

## Functionality 
###### Products
- Viewing product cards on the main page
- Filtering products by specs, price
- Searching for products
- Product detail page 
    - Viewing product images, expanded description
    - Comment section. Registered users are able to write comments and replies
    
###### Orders
- Adding/removing products in basket, changing quantity
- Viewing products in basket list and on checkout page
- Creating an order on the checkout page with customer data 
- Viewing order status in profile page (for signed in users)

###### Customers
- Sign up and sign in
- Profile page
    - Personal information, avatar
    - Viewing list of user's orders with their statuses
- Registered users are able to write comments on products and reply to other users
- Contacts page with the possibility to send an email to admins

###### Admin panel
- Standatd django admin panel
- Improved product admin page with the ability to see and modify
specs, description, images, comments, discount and other data of a product on a single page

###### API
- Allows requesting product list with pre-selected parameters to show 
- Create/update/delete products for admin and staff

## Setup
1. Install [docker-compose](https://docs.docker.com/compose/install/)
2. ```git clone https://github.com/mi-doc/emarket.git && cd emarket```
3. ```cat .env.sample >> .env ```
4. ```docker-compose -f docker-compose.prod.yml build```
5. ```docker-compose -f docker-compose.prod.yml up ```