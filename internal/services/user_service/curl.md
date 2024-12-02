## Users Service

### GET Request - Retrieve all users

```sh
curl -X GET "http://localhost:8001/api/users" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### GET Request - Retrieve a user by ID

```sh
curl -X GET "http://localhost:8001/api/users/7" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### POST Request - Create a new user

```sh
curl -X POST "http://localhost:8001/api/users" 
-H "Content-Type: application/json" \
-d '{
  "firstname": "sipaling",
  "lastname": "dota",
  "email": "mendota@example.com",
  "password": "mendota123",
  "confirm_password": "mendota123",
  "noc_transfer": "48285936453198575"
}'

```

### PUT Request - Update user information

```sh
curl -X PUT "http://localhost:8001/api/users/7" \
-H "Authorization: Bearer YOUR_BEARER_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "id": 7,
  "firstname": "sipaling",
  "lastname": "dota",
  "email": "mendota@example.com",
  "password": "mendota123",
  "confirm_password": "mendota123"
 
}'
```

### DELETE Request - Delete a user by ID

```sh
curl -X DELETE "http://localhost:8001/api/users/7" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```