# Emarket
##Table of contents
* [General info](#general info)
* [Technologies](#technologies)
* [Functionality](#functionality)
* [Setup](#setup)

##General info
Minimalistic online tablet store. 
Provides most basic functionality for customers and staff. 
This is a training project. 

##Technologies
- Python 3.8
- Django 3.0
- Django Rest Framework
- Javascript, jquery
- HTML, css
- PostgreSQL
- Nginx
- Docker

##Functionality 
###### Products
- Viewing product cards on the main page
- Filtering products by parameters, price
- Searching products 
- Product detail page 
    - Viewing product images, expanded description
    - Comment section. Registered users are able to write comments and replies
    
###### Orders
- Adding/removing products in basket, changing quantity
- Viewing products in basket list and on checkout page
- Creating an order on the checkout page with customer data 
- Viewing order status in profile page for registered users

###### Customers
- Sign up and sign in
- Profile page
    - Personal information, avatar
    - Viewing list of user's orders with their statuses
- Registered users are able to write comments to products and reply to other users
- Contacts page with the possibility to send an email to admins

###### API
- Allows requesting product list with pre-selected parameters to show 
- Create/update/delete products for admin and staff

##Setup
- Install [docker-compose](https://docs.docker.com/compose/install/)
- git clone https://github.com/mi-doc/emarket.git && cd emarket
- cat .env.sample >> .env 
- docker-compose -f docker-compose.prod.yml build
- docker-compose -f docker-compose.prod.yml up 