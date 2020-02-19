from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages

import pandas as pd
import psycopg2
import time
import re
import ast
import json
import time
from datetime import date
global sql_data_srting 

def index(request):
    sql_data = []
    time_start = time.time()
    flide1 = request.POST.get('flide')
    flide = str(flide1)
    num1 = str(request.POST.get('num1'))
    conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
    conn.set_client_encoding('UTF8')
    cur = conn.cursor() 
    # sqlText = 'SELECT * From book LIMIT 10;'
    if flide == "None" or num1 == "None":
        sqlText = 'SELECT * From book LIMIT 10;'
    else:
        sqlText = 'SELECT * From ' + flide + ' LIMIT 10;'
        if num1 != "":
            sqlText = 'SELECT * From ' + flide + ' LIMIT ' + num1 + ';'
        else:
            sqlText = 'SELECT * From ' + flide + ' LIMIT 1000 ;'
    ax1 = cur.execute(sqlText)
    data_dict = {}
    data_list = []
    count = 0
    if flide == 'book':
        for i in cur.fetchall():
            data_dict = {'id':i[0],'name':i[1],'page':i[2],'year':i[3]}
            data_list.append(data_dict)
    elif flide == 'author':
        for i in cur.fetchall():
            data_dict = {'name':i[0],'date':i[1]}
            data_list.append(data_dict)
    elif flide == 'publisher':
        for i in cur.fetchall():
            data_dict = {'name':i[0],'addr':i[1]}
            data_list.append(data_dict)
    else:
        for i in cur.fetchall():
            data_dict = {'id':i[0],'name':i[1],'page':i[2],'year':i[3]}
            data_list.append(data_dict)
    print(num1)
    time_stop = time.time()
    time_cou = time_stop - time_start
    context={
        'aa':["asd",'sss','ddd'],
        'data_list':data_list,
        'time_cou':time_cou,
        'flide':flide1
    }
    return render(request,'index.html',context)

def home(request):
    sql_data = []
    sql1 = request.POST.get('sq')
    sql_data_srting = str(sql1)
    context1={
        "sql_data_string":sql_data_srting
    }
    return render(request,'home.html',context1)

def singup(request):
    
    return render(request,'singin.html')

def login(request):
    return render(request,'login.html')

def view1(request):
    return render(request,'view.html')

def addu(request):
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    username = request.POST.get("username")
    password = request.POST.get("password")
    rpassword = request.POST.get("rpassword")
    email1 = request.POST.get("email1")

    if password == rpassword:
        if User.objects.filter(username=username).exists():
            # print("UserName already used")
            messages.info(request,"UserName already used")
            return redirect('/singup')
        elif User.objects.filter(email=email1).exists():
            # print("Email already used")
            messages.info(request,"Email already used")
            return redirect('/singup')
        else:
            user = User.objects.create_user(
                username = username,
                password = password,
                email=email1,
                first_name=firstname,
                last_name=lastname
            )
            user.save()
            return render(request,'adduser.html')
    else :
        # print("Password not match")
        messages.info(request,"Password not match")
        return redirect('/singup')

def loginw(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    #login (check user , password)
    user = auth.authenticate(username=username,password=password)

    if user is not None:
        auth.login(request,user)
        return redirect('/database')
    else:
        messages.info(request,"not found")
        return redirect('/login')

def logout(request):
    auth.logout(request)
    return redirect('/home')
