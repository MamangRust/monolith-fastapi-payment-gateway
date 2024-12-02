## Users Service

### GET Request - Retrieve all users

```sh
curl -X GET "http://localhost:8005/api/users" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### GET Request - Retrieve a user by ID

```sh
curl -X GET "http://localhost:8005/api/users/USER_ID" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### POST Request - Create a new user

```sh
curl -X POST "http://localhost:8005/api/users" \
-H "Authorization: Bearer YOUR_BEARER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "firstname": "FIRSTNAME",
    "lastname": "LASTNAME",
    "email": "EMAIL",
    "password": "PASSWORD",
    "confirm_password": "CONFIRM_PASSWORD",
    "noc_transfer": "OPTIONAL_NOC_TRANSFER_VALUE"
}'

```

### PUT Request - Update user information

```sh
curl -X PUT "http://localhost:8005/api/users/USER_ID" \
-H "Authorization: Bearer YOUR_BEARER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "firstname": "FIRSTNAME",
    "lastname": "LASTNAME",
    "email": "EMAIL",
    "password": "PASSWORD",
    "confirm_password": "CONFIRM_PASSWORD"
}'
```

### DELETE Request - Delete a user by ID


```sh
curl -X DELETE "http://localhost:8005/api/users/USER_ID" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```