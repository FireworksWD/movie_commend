# Generated by Django 3.2.9 on 2023-06-13 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.IntegerField(default=0, verbose_name='用户ID')),
                ('movieid', models.IntegerField(default=0, verbose_name='电影ID')),
                ('hitnum', models.IntegerField(default=0, verbose_name='点击次数')),
            ],
            options={
                'verbose_name': '点击量',
                'verbose_name_plural': '点击量',
            },
        ),
    ]
