# coding: UTF-8
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Person(models.Model):
    person = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    gender = models.CharField(
        choices=((u'男', '男'), (u'女', '女')),
        max_length=8,
        null=True,
    )
    institute = models.CharField(
        choices=(
            (u'信息与通信工程学院', '信息与通信工程学院'),
            (u'电子工程学院', '电子工程学院'),
            (u'计算机学院', '计算机学院'),
            (u'自动化学院', '自动化学院'),
            (u'数字媒体与设计艺术学院', '数字媒体与设计艺术学院'),
            (u'现代邮政学院', '现代邮政学院'),
            (u'网络空间安全学院', '网络空间安全学院'),
            (u'光电信息学院', '光电信息学院'),
            (u'理学院', '理学院'),
            (u'经济管理学院', '经济管理学院'),
            (u'公共管理学院', '公共管理学院'),
            (u'人文学院', '人文学院'),
            (u'国际学院', '国际学院'),
            (u'软件学院', '软件学院'),
        ),
        null=True,
        max_length=15
    )

    def __str__(self):
        return self.person.username + self.person.first_name
