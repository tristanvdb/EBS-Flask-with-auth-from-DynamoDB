EBauth
======

EBauth is a Flask server that uses DynamoDB to store the service's description and the users of this service.
The goal is to provide authentication in Flask applications deployed using Amazon's Elastic Beanstalk.

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


