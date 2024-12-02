# Saldo Service

## Sender

### GET Request - Get All Saldos

```sh
curl -X GET "http://localhost:8002/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Saldo by ID

```sh
curl -X GET "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldo by User ID

```sh
curl -X GET "http://localhost:8002/api/saldo/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldos for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8002/api/saldo/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Saldo

```sh
curl -X POST "http://localhost:8002/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "total_balance": 1000
}'
```

### PUT Request - Update an Existing Saldo

```sh
curl -X PUT "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "saldo_id": 1,
    "user_id": 1,
    "total_balance": 1500,
    "withdraw_amount": 200,
    "withdraw_time": "2024-12-02T10:00:00"
}'
```


### DELETE Request - Delete a Saldo by ID

```sh
curl -X DELETE "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"

```


## Receiver

### GET Request - Get All Saldos

```sh
curl -X GET "http://localhost:8002/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get a Single Saldo by ID

```sh
curl -X GET "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldo by User ID

```sh
curl -X GET "http://localhost:8002/api/saldo/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Saldos for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8002/api/saldo/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### POST Request - Create a New Saldo

```sh
curl -X POST "http://localhost:8002/api/saldo" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "total_balance": 1000
}'
```

### PUT Request - Update an Existing Saldo

```sh
curl -X PUT "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "saldo_id": 1,
    "user_id": 1,
    "total_balance": 1500,
    "withdraw_amount": 200,
    "withdraw_time": "2024-12-02T10:00:00"
}'
```


### DELETE Request - Delete a Saldo by ID

```sh
curl -X DELETE "http://localhost:8002/api/saldo/1" \
-H "Authorization: Bearer YOUR_TOKEN"

```