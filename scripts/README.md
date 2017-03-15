Scripts
=======

## Deploy

This script create the EBS application with a default environment.

```

```

## Create

This script create the service in the DynamoDB tables:
 * description in the `services` table
 * administrator in the `identities` table

```
Usage: create.py --service-name name
                 [--password-secret secret]
                 [--token-secret secret] [--token-timeout seconds]
                 [--admin-username username] [--admin-password password]
                 [--modules LIST]

Arguments:
  --service-name name   Name of the service being created
  --password-secret     Secret used to salt passwords (default: random string of length 16)
  --token-secret        Secret used to encode authentication tokens (default: random string of length 16)
  --token-timeout       Token timeout in seconds (default: 1 hour)
  --admin-username      Username for the administrator (default: "admin")
  --admin-password      Password for the administrator (default: random string of length 8)
  --modules LIST        Comma separated list of module to load (default: "EBauth.api.user" and "EBauth.api.test")
```

## WSGI

This script is launch an `EBauth` server locally. It is also the entry point for the default EBS.

```

```


