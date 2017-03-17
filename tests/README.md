Testing
=======

## Test Service

NOTE: Do not forget to start the VirtualEnv (`source .venv/bin/activate`)

### Create

```
python scripts/create.py --service-name your-service-name
```

### Local Server

```
python scripts/wsgi.py --service-name your-service-name
```

### Deploy with Elastic Beanstalk

TODO
TODO
TODO

### Remove

```
python scripts/create.py --service-name your-service-name
```

## Client

Test requests to a service. For local server:
```
tests/curl-tests.sh http://127.0.0.1:5000 admin SqcKrM+A
```
For local EBS:
```
tests/curl-tests.sh TODO admin SqcKrM+A
```
Expected output:
```
# Access no authentication
## Test public access
  > curl -s -X POST http://localhost:5000/tests/users/public
{
  "action": "public", 
  "api": "test", 
  "identity": null
}
## Test private access (FAIL)
  > curl -s -X POST http://localhost:5000/tests/users/private
Could not verify your access priviledge for that URL.

## Test admin access (FAIL)
  > curl -s -X POST http://localhost:5000/tests/users/admin
Could not verify your access priviledge for that URL.

# Admin authentication & token
## Test admin authentication
  > curl -s -X POST -u admin:iTZ+yOS6 http://localhost:5000/tests/users/admin
{
  "action": "admin", 
  "api": "test", 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
## Get token for admin
  > curl -s -X POST -u admin:iTZ+yOS6 http://localhost:5000/users/token | jq -r ".data | .token"
  Token: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk
## Test admin token through HTTP Auth field
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk: http://localhost:5000/tests/users/admin
{
  "action": "admin", 
  "api": "test", 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
## Test admin token through HTTP data
  > curl -s -X POST -d token=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk http://localhost:5000/tests/users/admin
{
  "action": "admin", 
  "api": "test", 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
# User management
## Add user0
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk: -d "user=user0&password=YY00&priviledges=user" http://localhost:5000/users/add
{
  "action": "add", 
  "api": "user", 
  "data": {
    "priviledges": [
      "user"
    ], 
    "user": "user0"
  }, 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
## Add user1
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk: -d "user=user1&password=YY11&priviledges=user" http://localhost:5000/users/add
{
  "action": "add", 
  "api": "user", 
  "data": {
    "priviledges": [
      "user"
    ], 
    "user": "user1"
  }, 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
## Add user1 (again: FAIL)
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk: -d "user=user1&password=YY11&priviledges=user" http://localhost:5000/users/add
{
  "action": "add", 
  "api": "user", 
  "data": {
    "error": "User user1 already exist!"
  }, 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
## Delete user1
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.3kg1F_v3yztogssuovlJlMfH0dd9A3HzKiIfJgE_DEk: -d "user=user1" http://localhost:5000/users/delete
{
  "action": "delete", 
  "api": "user", 
  "data": {
    "user": "user1"
  }, 
  "identity": {
    "priviledges": [
      "user", 
      "admin"
    ], 
    "user": "admin"
  }
}
# Test user tokens
## Get token for user0
  > curl -s -X POST -u user0:YY00 http://localhost:5000/users/token | jq -r ".data | .token"
  Token: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.IFETmqCDANIbp2TUud85YkE_zg2kUlFYJlmhD-nOlRg
## Test public access
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.IFETmqCDANIbp2TUud85YkE_zg2kUlFYJlmhD-nOlRg: http://localhost:5000/tests/users/private
{
  "action": "private", 
  "api": "test", 
  "identity": {
    "priviledges": [
      "user"
    ], 
    "user": "user0"
  }
}
## Test private access
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.IFETmqCDANIbp2TUud85YkE_zg2kUlFYJlmhD-nOlRg: http://localhost:5000/tests/users/private
{
  "action": "private", 
  "api": "test", 
  "identity": {
    "priviledges": [
      "user"
    ], 
    "user": "user0"
  }
}
## Test admin access (FAIL)
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTc3MzI5NywiaWF0IjoxNDg5NzY5Njk3fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.IFETmqCDANIbp2TUud85YkE_zg2kUlFYJlmhD-nOlRg: http://localhost:5000/tests/users/admin
Could not verify your access priviledge for that URL.


```
Expected logs on server side:
```
127.0.0.1 - - [17/Mar/2017 12:54:56] "POST /tests/users/public HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:56] "POST /tests/users/private HTTP/1.1" 401 -
127.0.0.1 - - [17/Mar/2017 12:54:56] "POST /tests/users/admin HTTP/1.1" 401 -
127.0.0.1 - - [17/Mar/2017 12:54:56] "POST /tests/users/admin HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/token HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /tests/users/admin HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /tests/users/admin HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/add HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/add HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/add HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/delete HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /users/token HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /tests/users/private HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /tests/users/private HTTP/1.1" 200 -
127.0.0.1 - - [17/Mar/2017 12:54:57] "POST /tests/users/admin HTTP/1.1" 401 -
```

NOTE: When authentication fails the server returns code 401.

