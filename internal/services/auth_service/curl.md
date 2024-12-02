# Auth Service

## User Sender

### POST Request - Register User

```sh
curl -X POST "http://localhost:8001/api/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "firstname": "John",
  "lastname": "Doe",
  "email": "john.doe@example.com",
  "password": "password123",
  "confirm_password": "password123"
}'
```

### POST Request - Login User

```sh
curl -X POST "http://localhost:8001/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "password123"
}'
```

## User Receiver

```sh
curl -X POST "http://localhost:8001/api/auth/register" \
-H "Content-Type: application/json" \
-d '{
  "firstname": "Jane",
  "lastname": "Doe",
  "email": "jane.doe@example.com",
  "password": "password123",
  "confirm_password": "password123"
}'
```

### POST Request - Login User

```sh
curl -X POST "http://localhost:8001/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "jane.doe@example.com",
  "password": "password123"
}'
```

---