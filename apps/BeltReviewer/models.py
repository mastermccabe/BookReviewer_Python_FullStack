from __future__ import unicode_literals
import bcrypt
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
# Create your models here.

class Validator(models.Manager):
    def validChecker(self, postData):
        errors = {}

        if len(postData['name']) < 2:
            errors["name"] = "Name no fewer than 2 characters"
            print errors
        if len(postData['alias']) < 2:
            errors["alias"] = "Alias no fewer than 2 characters"
            print errors
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "invalid email format"
        if len(postData['password']) < 8:
            errors["password"] = "Password must be no fewer than 8 characters in length"
            print errors

        if (postData['password'] != postData['conf_password']):
            errors["password"] = "passwords do not match"

        return errors

class Users(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = Validator()

class Authors(models.Model):
    author_name = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
class Books(models.Model):
    title = models.CharField(max_length=255)
    author_list = models.ForeignKey(Authors, related_name = "author")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    uploader = models.ForeignKey(Users, related_name = "uploaded_books")
    liked_users = models.ManyToManyField(Users, related_name = "liked_books")
class Reviews(models.Model):
    review = models.CharField(max_length=255)
    user_reviews = models.ForeignKey(Users, related_name = "User_reviews")
    rating = models.IntegerField()
    reviewed_book = models.ForeignKey(Books, related_name = "reviewed_book")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

# Authors.objects.create(author_name = "RL Stein")
# u = Authors.objects.get(id=1)

#
# Books.objects.get(id=1).author_list.all()[0].author_name
    # "author_name":Authors.objects.raw('SELECT id')
 # > python manage.py makemigrations
# > python manage.py migrate
# python manage.py shell
# from apps.Belt.models import *
    # Users.objects.all()

#  mac$ python manage.py makemigrations
#  $ python manage.py migrate
#  python manage.py shell
# from apps.Belt.models import *
# >>>
