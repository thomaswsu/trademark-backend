# Trademark-Backend!

Trademark-backend is the project making up the server and API to the Trademark project.

# Development Guide

## Install dependencies

```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
```

## Clone the Project

```bash
git clone https://github.com/thomaswsu/trademark-backend.git
```

## Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## Run the Server

```bash
python manage.py runserver
```

# Authorization

Authorization in Trademark is handled using JSON Web Tokens. The following steps can be completed to authenticate a user in Trademark.

- Create a new User
- Authenticate the User (Copy Access Token)
- Access a restricted endpoint (Include Access Token in  Authorization Header)

## Create a New User
```bash
curl --location --request POST 'http://127.0.0.1:8000/api/auth/new_user' \
--header 'Content-Type: application/json' \
--data-raw '{
	"email": <email>,
	"password": <password>,
	"first_name": <first-name>,
	"last_name": <last-name>
}'
```

## Authenticate User

```bash
curl --location --request POST 'http://127.0.0.1:8000/api/auth/token/' \
--header 'Content-Type: application/json' \
--data-raw '{
	"email": <email>,
	"password": <password>
}'
```

## Access Restricted Endpoint (ex: Get User)

Use the value of the "access" field returned by the token endpoint in the Authorization header for the GET user endpoint.

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/auth/user' \
--header 'Authorization: Bearer <access-token>'
```

## Update User Info

Update the user's email and password using the user PATCH endpoint. Each feild is optiona,
so you can update either the email, password, or both. Be sure to include the current password.

```bash
curl --location --request PATCH 'http://127.0.0.1:8000/api/auth/user' \
--header 'Authorization: Bearer <access-token>' \
--header 'Content-Type: application/json' \
--data-raw '{
	"password": <password>,
	"new_email": <new_email>,
	"new_password": <new_password>
}'
```

## Order Requests

To create a new order, the following request can be sent.

The action-type should be a "B" for a buy and "S" for a sell order.

The order-type should be one of the following: 'M' for 'Market', 'L' for 'Limit'

The execution-price is the price either set for a Limit order or the current price at time of a market order

The time-in-force can be one of the following options (refer to wikipedia for more info):
- 'GFD' for 'Good For Day',
- 'GTC' for 'Good Till Cancelled',
- 'IOC' for 'Immediate or Cancel',
- 'FOK' for 'Fill or Kill'

```bash
curl --location --request PUT 'http://127.0.0.1:8000/api/order' \     
--header 'Authorization: Bearer <access-token>' \
--header 'Content-Type: application/json' \
--data-raw '{
        "action_type": <action-type>,
		"order_type": <order-type>,
		"execution_price": <execution-price>,
		"time_in_force": <time-in-force>
}'
```

To get all orders, use the following endpoint. This will return a list of orders with their id and other useful info, for later use.
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/order/all' \
--header 'Authorization: Bearer <access-token>'
```

To get a specific order by id:
```bash
curl --location --request GET 'http://127.0.0.1:8000/api/order/<order-id>' \
--header 'Authorization: Bearer <access-token>'
```

Delete an order by id:

> This does not completely delete the order from the database, just cancels the order and relays that to the broker

To get a specific order by id:
```bash
curl --location --request DELETE 'http://127.0.0.1:8000/api/order/<order-id>' \
--header 'Authorization: Bearer <access-token>'
```
