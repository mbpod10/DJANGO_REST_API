# Django RESTful API

1. Requirements
   - Python (3.5, 3.6, 3.7, 3.8, 3.9)
   - Django (2.2, 3.0, 3.1)
2. Install (Perhaps in Virtual Environment)
   - `pip3 install djangorestframework`

# Getting Started

### Create Project

```
django-admin startproject <MY_PROJECT_NAME>
```

cd into project

### Migrate

```
python3 manage.py migrate
```

### Run Server to See if It Is Working

```
python3 manage.py runserver
```

### Create APP

```
python manage.py startapp <MY_APP_NAME>
```

### Create Super User

```
python3 manage.py createsuperuser
```

### Import Apps to Setting.py

In `django_api_project/django_api_project/setting.py` import `rest_framework` and the name of your app

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ############################
    'rest_framework',
    'api_basic'
]

```

## Create Models

in `django_api_project/api_basic/models.py` create desired models

```python
from django.db import models

# Create your models here.


class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

```

## Migrate Models

1. Run
   - `python3 manage.py makemigrations`
   - `python3 manage.py migrate`

## Import Models to admin

```python
from django.contrib import admin
from .models import Article
# Register your models here.

admin.site.register(Article)

```

# Create Serializer Class

Make a new file called `serializers.py` and create a new class

```python
from rest_framework import serializers
from .models import Article


class ArticleSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    date = serializers.DateTimeField()

    def create(self, validated_data):
        return Article.objects.create(validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.email = validated_data.get('email', instance.email)
        instance.date = validated_data.get('date', instance.date())

        instance.save()
        return instance

```

### Make a post request via python shell

`python3 manage.py shell`

1. `from api_basic.models import Article`
2. `from api_basics.serializers import ArticleSerializer`
3. `from rest_framework.renderers import JSONRenderer`
4. `from rest_framework.parsers import JSONParser`
5. ` a = Article(title = 'Article Title', author='Bar', email ='par@gmail.com')`
6. `a.save()`
7. `a = Article(title = 'Second Title 2', author='Howdy', email ='second2@gmail.com')`
8. `a.save()`
9. `serializer = ArticleSerializer(a)`
10. `serializer.data`

<b>OUTPUT:</b>

```js
Out[11]: {'title': 'Second Title 2', 'author': 'Howdy', 'email': 'second2@gmail.com', 'date': '2020-10-05T19:25:18.055948Z'}
```
