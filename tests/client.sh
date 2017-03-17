#!/bin/bash -e

url=$1
username=$2
password=$3

CPOST="curl -s -X POST"

echo "# Access no authentication"

echo "## Test public access"
echo "  > $CPOST $url/tests/users/public"
$CPOST $url/tests/users/public ; echo

echo "## Test private access (FAIL)"
echo "  > $CPOST $url/tests/users/private"
$CPOST $url/tests/users/private ; echo

echo "## Test admin access (FAIL)"
echo "  > $CPOST $url/tests/users/admin"
$CPOST $url/tests/users/admin ; echo

echo "# Admin authentication & token"

echo "## Test admin authentication"
echo "  > $CPOST -u $username:$password $url/tests/users/admin"
$CPOST -u $username:$password $url/tests/users/admin ; echo

echo "## Get token for admin"
echo "  > $CPOST -u $username:$password $url/users/token | jq -r \".data | .token\""
TOKEN=$($CPOST -u $username:$password $url/users/token | jq -r ".data | .token")
echo "  Token: $TOKEN"

echo "## Test admin token through HTTP Auth field"
echo "  > $CPOST -u $TOKEN: $url/tests/users/admin"
$CPOST -u $TOKEN: $url/tests/users/admin ; echo

echo "## Test admin token through HTTP data"
echo "  > $CPOST -d "token=$TOKEN" $url/tests/users/admin"
$CPOST -d "token=$TOKEN" $url/tests/users/admin ; echo

echo "# User management"

echo "## Add user0"
echo "  > $CPOST -u $TOKEN: -d \"user=user0&password=YY00&priviledges=user\" $url/users/add"
$CPOST -u $TOKEN: -d "user=user0&password=YY00&priviledges=user" $url/users/add ; echo

echo "## Add user1"
echo "  > $CPOST -u $TOKEN: -d \"user=user1&password=YY11&priviledges=user\" $url/users/add"
$CPOST -u $TOKEN: -d "user=user1&password=YY11&priviledges=user" $url/users/add ; echo

echo "## Add user1 (again: FAIL)"
echo "  > $CPOST -u $TOKEN: -d \"user=user1&password=YY11&priviledges=user\" $url/users/add"
$CPOST -u $TOKEN: -d "user=user1&password=YY11&priviledges=user" $url/users/add ; echo

echo "## Delete user1"
echo "  > $CPOST -u $TOKEN: -d \"user=user1\" $url/users/delete"
$CPOST -u $TOKEN: -d "user=user1" $url/users/delete ; echo

echo "# Test user tokens"

echo "## Get token for user0"
echo "  > $CPOST -u user0:YY00 $url/users/token | jq -r \".data | .token\""
TOKEN=$($CPOST -u user0:YY00 $url/users/token | jq -r ".data | .token")
echo "  Token: $TOKEN"

echo "## Test public access"
echo "  > $CPOST -u $TOKEN: $url/tests/users/private"
$CPOST -u $TOKEN: $url/tests/users/private ; echo

echo "## Test private access"
echo "  > $CPOST -u $TOKEN: $url/tests/users/private"
$CPOST -u $TOKEN: $url/tests/users/private ; echo

echo "## Test admin access (FAIL)"
echo "  > $CPOST -u $TOKEN: $url/tests/users/admin"
$CPOST -u $TOKEN: $url/tests/users/admin ; echo

