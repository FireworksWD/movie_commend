from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, reverse, HttpResponse
from movie_commend import settings
from movie.models import Movie
import os


def insertToSQL(fileName):
    txtfile = open(fileName, 'r', encoding='utf-8')
    for line in txtfile.readlines():
        try:
            movieinfo = line.split(',')
            id = movieinfo[0]
            name = movieinfo[1]
            rating = movieinfo[2]
            info = movieinfo[3]
            short = movieinfo[4]
            url = movieinfo[5]
            try:
                Movie.objects.create(movie_sort=id,movie_name=name, rating=rating, informations=info, short=short, url=url)
            except:
                print('save error' + id)
        except:
            print('read error')


def handle_upload_file(name, file):
    path = os.path.join(settings.BASE_DIR, 'uploads')
    fileName = path + '/' + name
    print(fileName)
    with open(fileName, 'wb') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    insertToSQL(fileName)


def importBookData(request):
    if request.method == 'POST':
        file = request.FILES.get('file', None)
        if not file:
            return HttpResponse('None File uploads !')
        else:
            name = file.name
            handle_upload_file(name, file)
            return redirect(reverse('index'))
    return render(request, 'utils/upload.html')


if __name__ == '__main__':
    pass
