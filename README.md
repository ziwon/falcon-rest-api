Falcon Template for REST API
============================
Simple Falcon Template with PostgreSQL for REST API (Falcon is a high-performance Python framework for building cloud APIs, smart proxies, and app backends. More information can be found [here](https://github.com/falconry/falcon/))


Requirements
============
Make sure that you have already the required packages installed before beginning.

Ubuntu
------

Update your system

```
sudo apt-get update
sudo apt-get upgrade
```

Install the required packages 

```
sudo apt-get install build-essential python-pip libffi-dev python-dev python3-dev libpq-dev
```

Mac
---

Install `postgres` for `psycopg2` dependency
```
brew update
brew install postgres
```


Installation
============

Install all the project dependencies in requirements.txt

```
  ./install.sh
```
Activate virtualenv

```
  .venv/bin/activate
```

Start service

```
  ./bin/run.sh start
```

Usage
=====

- Create user
```
curl -XPOST http://localhost:8000/v1/users -H "Content-Type: application/json" -d '{
 "username": "test1",
 "email": "test1@gmail.com",
 "password": "test1234"
}'
{
  "meta": {
    "code": 201
  }
}
```

- Login user
```
curl -XGET http://localhost:8000/v1/users/self/login -d email=test1@gmail.com -d password=test1234
{
  "id": "1",
  "username": "test1",
  "email": "test1@gmail.com",
  "modified": "2015-09-03 20:18:05.142613",
  "created": "2015-09-03 20:18:05.142613",
  "sid": "7027243698",
  "token": "gAAAAABV6Cxtz2qbcgOOzcjjyoBXBxJbjxwY2cSPdJB4gta07ZQXUU5NQ2BWAFIxSZlnlCl7wAwLe0RtBECUuV96RX9iiU63BP7wI1RQW-G3a1zilI3FHss="
}
```

- Get other user with auth token
```
curl -XGET http://localhost:8000/v1/users/100 -H "Authorization: gAAAAABV6Cxtz2qbcgOOzcjjyoBXBxJbjxwY2cSPdJB4gta07ZQXUU5NQ2BWAFIxSZlnlCl7wAwLe0RtBECUuV96RX9iiU63BP7wI1RQW-G3a1zilI3FHss="
{"message": "user not found (id: 100)"}
```
