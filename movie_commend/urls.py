"""movie_commend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from utils import views as utviews
from movie import views

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index, name='index'),
                  path('login/', views.log_in, name='login'),
                  path('register', views.register, name='register'),
                  path('captcha/', include('captcha.urls')),
                  path('log_out/', views.log_out, name='logout'),
                  path('updata/', utviews.importBookData, name='updata'),
                  path('recommend/', views.recommend_book, name='recommend'),
                  path('movieinfo/<int:id>', views.detail, name='movieinfo')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)