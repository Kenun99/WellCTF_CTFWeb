from django.db import models
import hashlib, os

from CTFWeb.settings import BASE_DIR
from account.models import Person
from django.contrib.auth.models import User


# Create your models here.
def get_upload_path(instance, filename):
    return instance.category + '/problems'.format(hashlib.md5(instance.name.encode('utf-8')).hexdigest(),
                                                  filename)


class Contest(models.Model):
    name = models.CharField(max_length=25, unique=True, default='')
    detail = models.CharField(max_length=300, unique=False, default='')
    datetime_begin = models.DateTimeField(null=True)
    datetime_end = models.DateTimeField(null=True)
    creator = models.CharField(max_length=25, default='root')

    def __str__(self):
        return self.name


class Problem(models.Model):
    name = models.CharField(max_length=25, unique=True, default='')
    detail = models.CharField(max_length=300, unique=False, default='')
    author = models.CharField(max_length=25, unique=False, default='unknown')
    bill = models.IntegerField(default=0)
    solvedCount = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    flag = models.CharField(max_length=80, unique=False, null=True, default='')
    file = models.FileField(null=True, blank=True, upload_to='problemFile/%Y-%m-%d')
    contest = models.ForeignKey(Contest, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Solved(models.Model):
    datetime_done = models.DateTimeField(null=True)
    res = models.IntegerField(default=0)
    problem_id = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    contest_id = models.IntegerField(default=0)
