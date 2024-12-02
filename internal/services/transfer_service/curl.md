# Transfer Service


## Sender

### GET Request - Get All Transfer

```sh
curl -X GET "http://localhost:8004/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### GET Request - Get a Single Transfer by ID

```sh
curl -X GET "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```


### GET Request - Get Transfer by User ID

```sh
curl -X GET "http://localhost:8004/api/transfer/user/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```


### GET Request - Get Transfer for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8004/api/transfer/users/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"


```

### POST Request - Create a New Transfer

```sh
curl -X POST "http://localhost:8004/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 123,
  "amount": 50000,
  "destination_account": "9876543210",
  "transfer_method": "bank_transfer"
}'
```


### PUT Request - Update an Existing Transfer

```sh
curl -X PUT "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "user_id": 123,
  "amount": 55000,
  "destination_account": "9876543210",
  "transfer_method": "bank_transfer"
}'
```


### DELETE Request - Delete a Transfer by ID

```sh
curl -X DELETE "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


## Receiver

### GET Request - Get All Transfer

```sh
curl -X GET "http://localhost:8004/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```


### GET Request - Get a Single Transfer by ID

```sh
curl -X GET "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```


### GET Request - Get Transfer by User ID

```sh
curl -X GET "http://localhost:8004/api/transfer/user/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"
```


### GET Request - Get Transfer for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8004/api/transfer/users/123" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"


```

### POST Request - Create a New Transfer

```sh
curl -X POST "http://localhost:8004/api/transfer" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "user_id": 123,
  "amount": 50000,
  "destination_account": "9876543210",
  "transfer_method": "bank_transfer"
}'
```


### PUT Request - Update an Existing Transfer

```sh
curl -X PUT "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json" \
-d '{
  "id": 1,
  "user_id": 123,
  "amount": 55000,
  "destination_account": "9876543210",
  "transfer_method": "bank_transfer"
}'
```


### DELETE Request - Delete a Transfer by ID

```sh
curl -X DELETE "http://localhost:8004/api/transfer/1" \
-H "Authorization: Bearer <your-token>" \
-H "Content-Type: application/json"

```
