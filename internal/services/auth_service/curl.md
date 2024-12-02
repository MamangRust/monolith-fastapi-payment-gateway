## Auth Service

### POST Request - Register User

```sh
curl -X POST "http://localhost:8001/api/auth/register" \
-H "Content-Type: application/json" \
-d '{
    "firstname": "FIRSTNAME",
    "lastname": "LASTNAME",
    "email": "EMAIL",
    "password": "PASSWORD",
    "confirm_password": "CONFIRM_PASSWORD"
}'
```

### POST Request - Login User

```sh
curl -X POST "http://localhost:8001/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
    "email": "EMAIL",
    "password": "PASSWORD"
}'
```