# Auth Service

## User Sender

### POST Request - Register User

```sh
curl -X POST "http://localhost:8080/api/auth/register" \
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
curl -X POST "http://localhost:8080/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "john.doe@example.com",
  "password": "password123"
}'
```

## User Receiver

```sh
curl -X POST "http://localhost:8080/api/auth/register" \
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
curl -X POST "http://localhost:8080/api/auth/login" \
-H "Content-Type: application/json" \
-d '{
  "email": "jane.doe@example.com",
  "password": "password123"
}'
```

---

# Users Service


### GET Request - Retrieve all users

```sh
curl -X GET "http://localhost:8080/api/users" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### GET Request - Retrieve a user by ID

```sh
curl -X GET "http://localhost:8080/api/users/7" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```

### POST Request - Create a new user

```sh
curl -X POST "http://localhost:8080/api/users" 
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
curl -X PUT "http://localhost:8080/api/users/7" \
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
curl -X DELETE "http://localhost:8080/api/users/7" -H "Authorization: Bearer YOUR_BEARER_TOKEN"
```
---

## Saldo Service

## Sender

### GET Request - Get All Saldos

```sh
curl -X GET "http://localhost:8080/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Saldo by ID

```sh
curl -X GET "http://localhost:8080/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldo by User ID

```sh
curl -X GET "http://localhost:8080/api/saldo/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldos for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/saldo/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Saldo

```sh
curl -X POST "http://localhost:8080/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "total_balance": 50000
}'
```

### PUT Request - Update an Existing Saldo

```sh
curl -X PUT "http://localhost:8080/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "saldo_id": 1,
  "user_id": 1,
  "total_balance": 50000,
  "withdraw_amount": 0,
  "withdraw_time": "2024-12-03T04:01:14.642Z"
}'
```

### DELETE Request - Delete a Saldo by ID

```sh
curl -X DELETE "http://localhost:8080/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"

```

## Receiver

### GET Request - Get All Saldos

```sh
curl -X GET "http://localhost:8080/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Saldo by ID

```sh
curl -X GET "http://localhost:8080/api/saldo/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldo by User ID

```sh
curl -X GET "http://localhost:8080/api/saldo/user/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldos for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/saldo/users/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Saldo

```sh
curl -X POST "http://localhost:8080/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 2,
    "total_balance": 50000
}'
```

### PUT Request - Update an Existing Saldo

```sh
curl -X PUT "http://localhost:8080/api/saldo/2" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "saldo_id": 2,
    "user_id": 2,
    "total_balance": 50000,
    "withdraw_amount": 0,
    "withdraw_time": "2024-12-02T10:00:00"
}'
```

### DELETE Request - Delete a Saldo by ID

```sh
curl -X DELETE "http://localhost:8080/api/saldo/2" \
-H "Authorization: Bearer YOUR_TOKEN"

```

---

# Topup Service

## Sender

### GET Request - Get All Topup

```sh
curl -X GET "http://localhost:8080/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Topup by ID

```sh
curl -X GET "http://localhost:8080/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup by User ID

```sh
curl -X GET "http://localhost:8080/api/topup/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/topup/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Topup

```sh
curl -X POST "http://localhost:8080/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "topup_no": "12333",
  "topup_amount": 50000,
  "topup_method": "ovo"
}'
```

### PUT Request - Update an Existing Topup

```sh
curl -X PUT "http://localhost:8080/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "topup_id": 1,
  "topup_amount": 50000,
  "topup_method": "ovo"
}'

```

### DELETE Request - Delete a Topup by ID

```sh
curl -X DELETE "http://localhost:8080/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

---

## Receiver

### GET Request - Get All Topup

```sh
curl -X GET "http://localhost:8080/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Topup by ID

```sh
curl -X GET "http://localhost:8080/api/topup/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup by User ID

```sh
curl -X GET "http://localhost:8080/api/topup/user/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/topup/users/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Topup

```sh
curl -X POST "http://localhost:8080/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 2,
  "topup_no": "12333",
  "topup_amount": 50000,
  "topup_method": "ovo"
}'
```

### PUT Request - Update an Existing Topup

```sh
curl -X PUT "http://localhost:8080/api/topup/2" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 2,
  "topup_id": 2,
  "topup_amount": 50000,
  "topup_method": "ovo"
}'

```

### DELETE Request - Delete a Topup by ID

```sh
curl -X DELETE "http://localhost:8080/api/topup/2" \
-H "Authorization: Bearer YOUR_TOKEN"
```

---

# Transfer Service

## Sender

### GET Request - Get All Transfer

```sh
curl -X GET "http://localhost:8080/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get a Single Transfer by ID

```sh
curl -X GET "http://localhost:8080/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```

### GET Request - Get Transfer by User ID

```sh
curl -X GET "http://localhost:8080/api/transfer/user/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```

### GET Request - Get Transfer for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/transfer/users/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"


```

### POST Request - Create a New Transfer

```sh
curl -X POST "http://localhost:8080/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "transfer_from": 1,
  "transfer_to": 2,
  "transfer_amount": 50000
}'
```

### PUT Request - Update an Existing Transfer

```sh
curl -X PUT "http://localhost:8080/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "transfer_id": 1,
  "transfer_from": 1,
  "transfer_to": 2,
  "transfer_amount": 50000
}'
```

### DELETE Request - Delete a Transfer by ID

```sh
curl -X DELETE "http://localhost:8080/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

## Receiver

### GET Request - Get All Transfer

```sh
curl -X GET "http://localhost:8080/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get a Single Transfer by ID

```sh
curl -X GET "http://localhost:8080/api/transfer/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```

### GET Request - Get Transfer by User ID

```sh
curl -X GET "http://localhost:8004/api/transfer/user/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```

### GET Request - Get Transfer for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/transfer/users/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"


```

### POST Request - Create a New Transfer

```sh
curl -X POST "http://localhost:8080/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "transfer_from": 2,
  "transfer_to": 1,
  "transfer_amount": 50000
}'
```

### PUT Request - Update an Existing Transfer

```sh
curl -X PUT "http://localhost:8080/api/transfer/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "transfer_id": 2,
  "transfer_from": 2,
  "transfer_to": 1,
  "transfer_amount": 50000
}'
```

### DELETE Request - Delete a Transfer by ID

```sh
curl -X DELETE "http://localhost:8080/api/transfer/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

---

# Withdraw Service

## Sender

### GET Request - Get All Withdraw

```sh
curl -X GET "http://localhost:8080/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get a Single Withdraw by ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw by User ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/user/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/users/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### POST Request - Create a New Withdraw

```sh
curl -X POST "http://localhost:8080/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "withdraw_amount": 50000,
  "withdraw_time": "2024-12-03T04:10:36.464Z"
}'

```

### PUT Request - Update an Existing Withdraw

```sh
curl -X PUT "http://localhost:8080/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 1,
  "withdraw_id": 1,
  "withdraw_amount": 50000,
  "withdraw_time": "2024-12-03T04:09:44.645Z"
}'

```

### DELETE Request - Delete a Withdraw by ID

```sh
curl -X DELETE "http://localhost:8080/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

## Receiver

### GET Request - Get All Withdraw

```sh
curl -X GET "http://localhost:8080/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get a Single Withdraw by ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw by User ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/user/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8080/api/withdraw/users/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### POST Request - Create a New Withdraw

```sh
curl -X POST "http://localhost:8080/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 2,
  "withdraw_amount": 50000,
  "withdraw_time": "2024-12-03T04:10:36.464Z"
}'

```

### PUT Request - Update an Existing Withdraw

```sh
curl -X PUT "http://localhost:8080/api/withdraw/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 2,
  "withdraw_id": 2,
  "withdraw_amount": 50000,
  "withdraw_time": "2024-12-03T04:09:44.645Z"
}'

```

### DELETE Request - Delete a Withdraw by ID

```sh
curl -X DELETE "http://localhost:8080/api/withdraw/2" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

---
