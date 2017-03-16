EBS: Flask server with authentication through DynamoDB
======================================================

This code shows how to deploy a Flask server on AWS' Elastic Beanstalk. This server provides authentication through DynamoDB. It also implement token based authentication.

## Dependencies

 * `python 2.7`
 * `virtualenv`
 * `jq` (for tests)

### Deploy

TODO

```
zip EBS-Flask-with-auth-from-DynamoDB.zip .ebextensions/python.config requirements.txt
zip EBS-Flask-with-auth-from-DynamoDB.zip server/*.py server/api/*.py
zip EBS-Flask-with-auth-from-DynamoDB.zip static/...
zip EBS-Flask-with-auth-from-DynamoDB.zip templates/...
```


