# Topup Service

## Sender

### GET Request - Get All Topup

```sh
curl -X GET "http://localhost:8003/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### GET Request - Get a Single Topup by ID

```sh
curl -X GET "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup by User ID

```sh
curl -X GET "http://localhost:8003/api/topup/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### GET Request - Get Topup for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8003/api/topup/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### POST Request - Create a New Topup

```sh
curl -X POST "http://localhost:8003/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "topup_no": "TOPUP12345",
    "topup_amount": 50000,
    "topup_method": "dana"
}'
```


### PUT Request - Update an Existing Topup

```sh
curl -X PUT "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "topup_id": 1,
    "topup_amount": 45000,
    "topup_method": "ovo"
}'

```


### DELETE Request - Delete a Topup by ID

```sh
curl -X DELETE "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

------------------------------

## Receiver


### GET Request - Get All Topup

```sh
curl -X GET "http://localhost:8003/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### GET Request - Get a Single Topup by ID

```sh
curl -X GET "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```

### GET Request - Get Topup by User ID

```sh
curl -X GET "http://localhost:8003/api/topup/user/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### GET Request - Get Topup for Multiple Users by User ID

```sh
curl -X GET "http://localhost:8003/api/topup/users/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```


### POST Request - Create a New Topup

```sh
curl -X POST "http://localhost:8003/api/topup" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "topup_no": "TOPUP12345",
    "topup_amount": 50000,
    "topup_method": "dana"
}'
```


### PUT Request - Update an Existing Topup

```sh
curl -X PUT "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
    "user_id": 1,
    "topup_id": 1,
    "topup_amount": 45000,
    "topup_method": "ovo"
}'

```


### DELETE Request - Delete a Topup by ID

```sh
curl -X DELETE "http://localhost:8003/api/topup/1" \
-H "Authorization: Bearer YOUR_TOKEN"
```
