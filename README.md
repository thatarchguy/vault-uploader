Overview
========

A package to upload config ini files to [Hashicorp's Vault](https://github.com/hashicorp/vault/)

```
$ vault-uploader --help
Usage: vault-uploader [OPTIONS] FILENAME

Options:
  --vault_server TEXT     The Vault server address
  --vault_namespace TEXT  The application namespace in Vault
  --vault_env TEXT        The application environment (pilot, prod, etc..)
  --vault_token TEXT      Your Vault server token
  --help                  Show this message and exit.
```


Purpose
=======

It will take a file in this format:
```
[database]
username = test
password = test

[redis]
host = redis.server.test
```

namespace = myapp
env = prod

and upload into Vault like this:

```
myapp/prod/database
{
    "username": "test",
    "password": " test"
}

myapp/prod/redis
{
    "host": "redis.server.test"
}
```


Installation
============
```
pip install vault-uploader
```
