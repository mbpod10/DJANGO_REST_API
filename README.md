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

11. `content = JSONRenderer().render(serializer.data)`
12. `content`

<b>OUTPUT:</b>

```js
//Serialized Data
 b'{"title":"Second Title 2","author":"Howdy","email":"second2@gmail.com","date":"2020-10-05T19:25:18.055948Z"}'

```

13. `serializer = ArticleSerializer(Article.objects.all(), many=True)`
14. `serializer.data`

<b>OUTPUT:</b>

```js
[
  OrderedDict([
    ("title", "Article Title"),
    ("author", "Bar"),
    ("email", "par@gmail.com"),
    ("date", "2020-10-05T19:21:45.766033Z"),
  ]),
  OrderedDict([
    ("title", "Second Title 2"),
    ("author", "Howdy"),
    ("email", "second2@gmail.com"),
    ("date", "2020-10-05T19:25:18.055948Z"),
  ]),
];
```

Do this in `serializers.py`

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'email', 'date']
```

<b> THESE ARE THE FIELDS THAT WILL BE SHOWN AS THE API</b>

PYTHON SHELL

1.  `serializer = ArticleSerializer()`
2.  `print(repr(serializer))`

<b>OUTPUT</b>

```
ArticleSerializer():
    title = CharField(max_length=100)
    author = CharField(max_length=100)
    email = EmailField(max_length=100)
    date = DateTimeField()
```

# Views

In order to tell our server what we want to see, we need to create a method that shows all the articles in our API. It works like an index route. Both `POST` and `GET` are usually used through the same url endpoint. Think the following method as an index route for the Article model. <br  />

in `views.py`

```python
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
# Create your views here.


def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ArticleSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

```

- Notice the serializers are imported to the file

# Urls

We want a seperate url path for articles so we need to add `path("", include('api_basic.urls'))` in the `url.py` in the project folder.

Include `api_baiscs.urls` in `django_api_projects` urls

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('api_basic.urls'))
]

```

create a new file called `urls.py` in `api_basic` and render the function that was created in `views.py` <br  />
These routes will be imported to the `project/urls.py`

```python
from django.urls import path, include
from .views import article_list
urlpatterns = [
    path('article/', article_list),
]
```

Go to http://127.0.0.1:8000/article/

<b>OUTPUT</b>

```json
[
  {
    "id": 1,
    "title": "Article Title",
    "author": "Bar",
    "email": "par@gmail.com",
    "date": "2020-10-05T19:21:45.766033Z"
  },
  {
    "id": 2,
    "title": "Second Title 2",
    "author": "Howdy",
    "email": "second2@gmail.com",
    "date": "2020-10-05T19:25:18.055948Z"
  }
]
```

## Postman

run a `GET` request from `http://localhost:8000/article`

<b>OUTPUT</b>

```json
[
  {
    "id": 1,
    "title": "Article Title",
    "author": "Bar",
    "email": "par@gmail.com",
    "date": "2020-10-05T19:21:45.766033Z"
  },
  {
    "id": 2,
    "title": "Second Title 2",
    "author": "Howdy",
    "email": "second2@gmail.com",
    "date": "2020-10-05T19:25:18.055948Z"
  }
]
```

Nice, now lets run a post request via PostMan

1. open postman to `POST`
2. make sure the url post is `http://localhost:8000/article/`
3. click `Body`
4. click `Raw`
5. on the right, Select `JSON` from the dropdown
6. insert the following:

```json
{
  "id": 3,
  "title": "Article Title3",
  "author": "Three",
  "email": "three@gmail.com"
}
```

## Error

Internal Error, we need to fix the csrf

## Solved

`api_basics/views.py` import `from django.views.decorators.csrf import csrf_exempt` and add the instance `@csrf_exempt` above the `article_list` function

<b>NEW POST SUCCESSFUL</b> <br  />

Now go back to `http://127.0.0.1:8000/article/`

<b>Output</b>

```json
[
  {
    "id": 1,
    "title": "Article Title",
    "author": "Bar",
    "email": "par@gmail.com",
    "date": "2020-10-05T19:21:45.766033Z"
  },
  {
    "id": 2,
    "title": "Second Title 2",
    "author": "Howdy",
    "email": "second2@gmail.com",
    "date": "2020-10-05T19:25:18.055948Z"
  },
  {
    "id": 3,
    "title": "Article Title3",
    "author": "Three",
    "email": "three@gmail.com",
    "date": "2020-10-05T21:26:52.404102Z"
  }
]
```
