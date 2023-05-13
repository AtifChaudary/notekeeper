# NoteKeeper

## - Python 3.9

## - Django 4.2.1

##### Installation

To install virtualenv via pip run:

```bash
pip install virtualenv
```

##### Usage

Creation of virtualenv:

```bash
virtualenv -p python3 <desired-path>
```

Activate the virtualenv:

```bash
source <desired-path>/bin/activate
```

Deactivate the virtualenv:

```bash
deactivate
```

Run Server:

```bash
python manage.py runserver
```


Run Test Cases:

```bash
python manage.py test
```

## - Docker

Build:
    docker build . -t docker-django-v0.1
Run: 
    docker run docker-django-v0.1 