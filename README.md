# 🍹 Aperol

A backend for movemaison.com

### Developer setup

Have some version of Postgres installed. I prefer Postgres.app, but `postgresql`
is a good choice too.

Make sure that you have all the necessary libraries install for GeoDjango:

```
$ brew install postgis gdal libgeoip
```

Create a superuser called `aperol`.

```
$ createuser -s aperol
```

Create a database called `movemaison` with `aperol` as the owner.

```
$ createdb movemaison -O aperol
```

Create a virtual environment, and activate it.

```
# assuming python is an alias for python3
$ python -m venv venv
$ source venv/bin/activate
```

Install the requirements.

```
$ pip install -r requirements.txt
```

Migrate.

```
$ python manage.py migrate
```

Run the server.

```
$ python manage.py runserver
```
