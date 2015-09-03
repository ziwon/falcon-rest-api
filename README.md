Falcon Template for REST API
============================
Simple Falcon Template with PostgreSQL for REST API


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
  sudo apt-get install build-essential python3-dev python-pip libpq-dev
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
