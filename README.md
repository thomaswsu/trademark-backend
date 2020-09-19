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
	"username": <username>,
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
	"username": <username>,
	"password": <password>
}'
```

## Access Restricted Endpoint (ex: Get User)

Use the value of the "access" field returned by the token endpoint in the Authorization header for the GET user endpoint.

```bash
curl --location --request GET 'http://127.0.0.1:8000/api/auth/user' \
--header 'Authorization: Bearer <access-token>'
```
