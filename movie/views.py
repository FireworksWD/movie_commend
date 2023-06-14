from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from movie.reg_login_forms.register_forms import Reg_Form
from movie.models import BookUser, Movie, hits
from movie.reg_login_forms.login import Login_Form

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.


from recommed import recommend
import redis

pool = redis.ConnectionPool(host='192.168.188.20', port=6379)
redis_client = redis.Redis(connection_pool=pool)


def recommend_book(request):
    import re
    if request.user.is_authenticated:
        userid = request.user.id
        recommend.getRecommendByUserID(userid, 6)
        print('当前用户', userid)
        recommend_result = redis_client.get(userid)
        print('结果', recommend_result)
        movielist = str(recommend_result).split(',')
        if movielist[0] != "None":
            movieset = []
            for mv in movielist[:-1]:
                res = re.findall(r'\d+', mv)[0]
                x = Movie.objects.get(movie_sort=int(res))
                movieset.append(x)
            return render(request, 'home/recommend.html', locals())
        else:
            movieset = Movie.objects.order_by('rating')[:4]
            return render(request, 'home/recommend.html', locals())
    else:
        return redirect(reverse('login'))


def detail(request, id):
    mv = Movie.objects.get(id=id)
    currentuser = request.user.id
    if currentuser:
        try:
            hit = hits.objects.get(userid=currentuser, movieid=id)
            hit.hitnum += 1
            hit.save()
            print(hit)
        except hits.DoesNotExist:
            hit2 = hits()
            hit2.userid = currentuser
            hit2.movieid = id
            hit2.hitnum += 1
            hit2.save()
            print(hit2)
        data = str(currentuser) + '\t' + str(id) + '\t' + str(1) + '\n'
        from hdfs import Client
        from utils import tools
        hdfs_path = '/movie/hits.txt'
        client = Client('http://node1:9870')
        tools.append_to_hdfs(client, hdfs_path, data)
        return render(request, 'home/detail.html', locals())
    else:
        return redirect(reverse('login'))


def index(request):
    import random
    rom = [random.randint(0, 249) for i in range(5)]
    movies1 = []
    for i in rom:
        temp = Movie.objects.get(movie_sort=i)
        movies1.append(temp)
    movies = Movie.objects.alias()
    paginator = Paginator(movies, 12)  # 每页显示  条数据
    page = request.GET.get('page')
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # 如果 page 不是整数，返回第一页
        movies = paginator.page(1)
    except EmptyPage:
        # 如果请求的页超出了范围，返回最后一页
        movies = paginator.page(paginator.num_pages)
    return render(request, 'home/index.html', locals())


def log_in(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms_l = Login_Form()
            return render(request, 'auth/login.html', locals())
        elif request.method == 'POST':
            forms_l = Login_Form(request.POST)
            if forms_l.is_valid():
                user = forms_l.cleaned_data['user']
                pwd = forms_l.cleaned_data['pwd']
                print(user, pwd)
                user1 = authenticate(request, username=user, password=pwd)
                if user1:
                    login(request, user1)
                elif not user1:
                    pwderr = '用户名密码错误'
                    return render(request, 'auth/login.html', locals())
                return redirect(reverse('index'))
            else:
                return render(request, 'auth/login.html', locals())
    else:
        return render(request, 'home/index.html')


def register(request):
    if not request.user.is_authenticated:
        if request.method == 'GET':
            forms = Reg_Form()
            return render(request, 'auth/register.html', locals())
        elif request.method == 'POST':
            forms = Reg_Form(request.POST)
            if forms.is_valid():
                user = forms.cleaned_data['username']
                pwd = forms.cleaned_data['pwd']
                gender = forms.cleaned_data['gender']
                birthday = forms.cleaned_data['birehday']
                phone = forms.cleaned_data['phone']
                BookUser.objects.create_user(username=user, password=pwd,
                                             gender=gender, birthday=birthday, phone=phone)
                return redirect(reverse('login'))
            else:
                return render(request, 'auth/register.html', locals())
    else:
        return HttpResponse('你已经登陆了')


def log_out(request):
    logout(request)
    return redirect(reverse('index'))
