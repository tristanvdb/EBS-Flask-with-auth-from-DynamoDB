EBS: Flask server with authentication through DynamoDB
======================================================

This code shows how to deploy a Flask server on AWS' Elastic Beanstalk. This server provides authentication through DynamoDB. It also implement token based authentication.

## Getting Started

### AWS setup

Create the table in DynamoDB:
 * `services` : to store information about service (secrets, ...). It has one key `service`.
 * `identities` : to store information about users of each service (priviledges, ...). It has two keys: `service` and `user`.

### Create a service

Simply run:
```
python scripts/create.py --service-name your-service-name
```
You might need to set the AWS\_PROFILE and AWS\_REGION environment variables.


Checkout the service configuration (includes randomly generated administrator password):
```
cat your-service-name.txt
```

### Local service

```
export PYTHONPATH=$(pwd):$PYTHONPATH # EBauth top directory
export SERVER_SERVICE=your-service-name
python scripts/wsgi.py
```
You might need to set the AWS\_PROFILE and AWS\_REGION environment variables.

### Try

Test public access:
 * `curl -X POST http://127.0.0.1:5000/api/test/public`

Test private/admin access (SHOULD FAIL):
 * `curl -X POST http://127.0.0.1:5000/api/test/private`
 * `curl -X POST http://127.0.0.1:5000/api/test/admin`

Test authentication (password in `your-service-name.txt`):
 * `curl -u admin:XXXXXXXX -X POST http://127.0.0.1:5000/api/test/private`
 * `curl -u admin:XXXXXXXX -X POST http://127.0.0.1:5000/api/test/admin`

Add users:
 * `curl -u admin:XXXXXXXX -d "user=user0&password=YYYY&priviledges=user" -X POST http://127.0.0.1:5000/api/user/add`
 * `curl -u admin:XXXXXXXX -d "user=user1&password=YYYY&priviledges=user" -X POST http://127.0.0.1:5000/api/user/add`

Delete user:
 * `curl -u admin:XXXXXXXX -d "user=user1" -X POST http://127.0.0.1:5000/api/user/delete`

Test tokens:
 * `curl -u user0:YYYY -X POST http://127.0.0.1:5000/api/user/token`
 * `curl -u TOKEN -X POST http://127.0.0.1:5000/api/test/private`
 * `curl -d "token=TOKEN" -X POST http://127.0.0.1:5000/api/test/private`

### Deploy

TODO

```
zip EBS-Flask-with-auth-from-DynamoDB.zip .ebextensions/python.config requirements.txt
zip EBS-Flask-with-auth-from-DynamoDB.zip server/*.py server/api/*.py
zip EBS-Flask-with-auth-from-DynamoDB.zip static/...
zip EBS-Flask-with-auth-from-DynamoDB.zip templates/...
```


