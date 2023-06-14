from django.db import models
from django.contrib.auth.models import AbstractUser
from movie.Storage import ImageStorage


# Create your models here.

class BookUser(AbstractUser):
    phone = models.CharField(verbose_name='手机号', max_length=11)
    choice_gender = (
        (0, '女'),
        (1, '男'),
        (2, '未知')
    )
    gender = models.IntegerField(verbose_name='性别', choices=choice_gender, default=3)
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)


class Movie(models.Model):
    movie_sort = models.IntegerField(verbose_name='排名', blank=False, default='')
    movie_name = models.CharField(verbose_name='电影名称', max_length=64, blank=False, default='')
    rating = models.FloatField(verbose_name='评分', max_length=5, default='0')
    informations = models.CharField(verbose_name='信息', max_length=200, default='')
    short = models.CharField(verbose_name='短评', max_length=64, default='')
    url = models.URLField(verbose_name='URL', blank=True, default='')
    cover = models.ImageField(verbose_name='封面', upload_to='images/%Y/%m/%d', default='images/default.png',
                              storage=ImageStorage)

    def __str__(self):
        return self.movie_name

    class Meta:
        verbose_name = '电影管理'
        verbose_name_plural = '电影管理'


class hits(models.Model):
    userid = models.IntegerField(verbose_name='用户ID', default=0)
    movieid = models.IntegerField(verbose_name='电影ID', default=0)
    hitnum = models.IntegerField(verbose_name='点击次数', default=0)

    def __str__(self):
        return str(self.userid)

    class Meta:
        verbose_name = '点击量'
        verbose_name_plural = '点击量'
