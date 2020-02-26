"""databasewebapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from blogs import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.home),
    path('database/', views.index),
    path('singup/', views.singup),
    path('login/', views.login),
    path('view/', views.view1),
    path('singup/adduser', views.addu),
    path('login/loginw', views.loginw),
    path('logout/', views.logout),
    path('query/', views.query),
    path('insert/', views.insert),
    path('insert/Ibook', views.ibook),
    path('insert/Iauthor', views.iauthor),
    path('insert/Ipublisher', views.ipublisher),
    path('query/Qdele', views.qdele),
    path('search/', views.search),
]
