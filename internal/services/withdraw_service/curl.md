# Withdraw Service


## Sender

### GET Request - Get All Withdraw

```sh
curl -X GET "http://localhost:8006/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### GET Request - Get a Single Withdraw by ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw by User ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/user/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```



### GET Request - Get Withdraw for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/users/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### POST Request - Create a New Withdraw


```sh
curl -X POST "http://localhost:8006/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 123,
  "amount": 25000,
  "destination_account": "9876543210",
  "withdraw_method": "bank_transfer"
}'

```


### PUT Request - Update an Existing Withdraw

```sh
curl -X PUT "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "user_id": 123,
  "amount": 30000,
  "destination_account": "9876543210",
  "withdraw_method": "bank_transfer"
}'

```


### DELETE Request - Delete a Withdraw by ID

```sh
curl -X DELETE "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```



## Receiver

### GET Request - Get All Withdraw

```sh
curl -X GET "http://localhost:8006/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### GET Request - Get a Single Withdraw by ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

### GET Request - Get Withdraw by User ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/user/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```



### GET Request - Get Withdraw for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8006/api/withdraw/users/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### POST Request - Create a New Withdraw


```sh
curl -X POST "http://localhost:8006/api/withdraw" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 123,
  "amount": 25000,
  "destination_account": "9876543210",
  "withdraw_method": "bank_transfer"
}'

```


### PUT Request - Update an Existing Withdraw

```sh
curl -X PUT "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "user_id": 123,
  "amount": 30000,
  "destination_account": "9876543210",
  "withdraw_method": "bank_transfer"
}'

```


### DELETE Request - Delete a Withdraw by ID

```sh
curl -X DELETE "http://localhost:8006/api/withdraw/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```

