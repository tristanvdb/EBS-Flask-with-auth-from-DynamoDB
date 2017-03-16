Tests scripts
=============

## Local Environment

Setup test environment (VirtualEnv).
```
tests/setup.sh
```

NOTE: You can specify AWS environment directly in your virtual environment:
```
echo -e "\nexport AWS_PROFILE=your-profile AWS_REGION=some-region" >> .venv/bin/activate
```

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
  > curl -s -X POST http://127.0.0.1:5000/api/test/public
{
  "action": "public", 
  "api": "test", 
  "identity": null
}
## Test private access (FAIL)
  > curl -s -X POST http://127.0.0.1:5000/api/test/private
Could not verify your access priviledge for that URL.

## Test admin access (FAIL)
  > curl -s -X POST http://127.0.0.1:5000/api/test/admin
Could not verify your access priviledge for that URL.

# Admin authentication & token
## Test admin authentication
  > curl -s -X POST -u admin:l5ppNfBt http://127.0.0.1:5000/api/test/admin
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
  > curl -s -X POST -u admin:l5ppNfBt http://127.0.0.1:5000/api/user/token | jq -r ".data | .token"
  Token: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs
## Test admin token through HTTP Auth field
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs: http://127.0.0.1:5000/api/test/admin
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
  > curl -s -X POST -d token=eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs http://127.0.0.1:5000/api/test/admin
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs: -d "user=user0&password=YY00&priviledges=user" http://127.0.0.1:5000/api/user/add
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs: -d "user=user1&password=YY11&priviledges=user" http://127.0.0.1:5000/api/user/add
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs: -d "user=user1&password=YY11&priviledges=user" http://127.0.0.1:5000/api/user/add
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIiwiYWRtaW4iXSwidXNlciI6ImFkbWluIn0.BqLCDkVU7GKi4Jzntxcls2ku4XMnrZy4SSH-U8spxWs: -d "user=user1" http://127.0.0.1:5000/api/user/delete
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
  > curl -s -X POST -u user0:YY00 http://127.0.0.1:5000/api/user/token | jq -r ".data | .token"
  Token: eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.3dHgHFwDYVHW9sglvSlsMuEzHWkIFjrQv_t2kfV6_-c
## Test public access
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.3dHgHFwDYVHW9sglvSlsMuEzHWkIFjrQv_t2kfV6_-c: http://127.0.0.1:5000/api/test/private
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.3dHgHFwDYVHW9sglvSlsMuEzHWkIFjrQv_t2kfV6_-c: http://127.0.0.1:5000/api/test/private
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
  > curl -s -X POST -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ4OTcwMTI3NiwiaWF0IjoxNDg5Njk3Njc2fQ.eyJwcml2aWxlZGdlcyI6WyJ1c2VyIl0sInVzZXIiOiJ1c2VyMCJ9.3dHgHFwDYVHW9sglvSlsMuEzHWkIFjrQv_t2kfV6_-c: http://127.0.0.1:5000/api/test/admin
Could not verify your access priviledge for that URL.

```
Expected logs on server side:
```
127.0.0.1 - - [16/Mar/2017 16:54:35] "POST /api/test/public HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:35] "POST /api/test/private HTTP/1.1" 401 -
127.0.0.1 - - [16/Mar/2017 16:54:35] "POST /api/test/admin HTTP/1.1" 401 -
127.0.0.1 - - [16/Mar/2017 16:54:35] "POST /api/test/admin HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/token HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/test/admin HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/test/admin HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/add HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/add HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/add HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/delete HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/user/token HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/test/private HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/test/private HTTP/1.1" 200 -
127.0.0.1 - - [16/Mar/2017 16:54:36] "POST /api/test/admin HTTP/1.1" 401 -
```

NOTE: When authentication fails the server returns code 401.

