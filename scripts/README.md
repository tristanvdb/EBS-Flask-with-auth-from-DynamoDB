Scripts
=======

## Create

This script creates the service in the DynamoDB tables:
 * description in the `services` table
 * administrator in the `identities` table

```
Usage: create.py [-h] --service-name name
                 [--password-secret secret]
                 [--token-secret secret] [--token-timeout seconds]
                 [--admin-username username] [--admin-password password]
                 [--modules LIST]
                 [--aws-profile profile] [--aws-region region]

Arguments:
  --service-name        Name of the service being created

  --password-secret     Secret used to salt passwords (default: random string of length 16)

  --token-secret        Secret used to encode authentication tokens (default: random string of length 16)
  --token-timeout       Token timeout in seconds (default: 1 hour)

  --admin-username      Username for the administrator (default: "admin")
  --admin-password      Password for the administrator (default: random string of length 8)

  --modules             Comma separated list of module to load (default: "EBauth.api.user" and "EBauth.api.test")

  --aws-profile         AWS profile to use (Default: env[AWS_PROFILE])
  --aws-region          AWS region to use (Default: env[AWS_REGION])
```

## Remove

This script removes the service from the DynamoDB tables:
 * description from the `services` table
 * all users from the `identities` table

```
Usage: remove.py --service-name name
                 [--aws-profile profile] [--aws-region region]

Arguments:
  --service-name        Name of the service being created

  --aws-profile         AWS profile to use (Default: env[AWS_PROFILE])
  --aws-region          AWS region to use (Default: env[AWS_REGION])
```

## WSGI

This script is launch an `EBauth` server locally. It is also the entry point for the default EBS.

```
Usage: wsgi.py [--service-name name]
               [--debug]
               [--aws-profile profile] [--aws-region region]

Arguments:
  --service-name        Name of the service being created (Default: env[EBAUTH_SERVICE_NAME])

  --debug               Launch Flask in debug mode

  --aws-profile         AWS profile to use (Default: env[AWS_PROFILE])
  --aws-region          AWS region to use (Default: env[AWS_REGION])
```

## Deploy

This script create the EBS application with a default environment.

```

```


