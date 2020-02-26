from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages

import psycopg2
import time
import time
from datetime import date
global sql_data_srting 

def index(request):
    sql_data = []
    count1 = []
    time_start = time.time()
    flide1 = request.POST.get('flide')
    flide = str(flide1)
    num1 = str(request.POST.get('num1'))
    conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
    conn.set_client_encoding('UTF8')
    cur = conn.cursor() 
    curb = conn.cursor() 
    cura = conn.cursor() 
    curp = conn.cursor() 
    sqlText_b = 'SELECT count(b_id) From book ;'
    sqlText_a = 'SELECT count(a_name) From author ;'
    sqlText_p = 'SELECT count(p_name) From publisher ;'
    curb.execute(sqlText_b)
    cura.execute(sqlText_a)
    curp.execute(sqlText_p)
    count1.append(curb.fetchall()[0][0])
    count1.append(cura.fetchall()[0][0])
    count1.append(curp.fetchall()[0][0])
    # sqlText = 'SELECT * From book LIMIT 10;'
    if flide == "None" or num1 == "None":
        sqlText = 'SELECT * From book LIMIT 10;'
    else:
        sqlText = 'SELECT * From ' + flide + ' LIMIT 10;'
        if num1 != "":
            sqlText = 'SELECT * From ' + flide + ' LIMIT ' + num1 + ';'
        else:
            sqlText = 'SELECT * From ' + flide + ' LIMIT 10000 ;'
    ax1 = cur.execute(sqlText)
    data_dict = {}
    data_list = []
    count = 0
    if flide == 'book':
        for i in cur.fetchall():
            data_dict = {'id':i[0],'name':i[1],'page':i[2],'year':i[3],'pb':i[4]}
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
        'flide':flide1,
        'count1':count1
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


def query(request):
    sql_text = str(request.POST.get('sql_text'))
    conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
    conn.set_client_encoding('UTF8')
    cur = conn.cursor()
    try:
        if sql_text == "None":
            sql_text = 'SELECT * From book LIMIT 10; '
            cur.execute(sql_text)
        else:
            sql_text = sql_text
            cur.execute(sql_text)
    except psycopg2.Error as error:
        messages.info(request,"Syntax Error")
        return redirect('/query')
    sql_list=cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    context = {
        'sql_list':sql_list,
        'colnames':colnames,
        'sql_text':sql_text
    }


    return render(request,'query.html',context)

def insert(request):

    flide1 = request.POST.get('flide')
    flide = str(flide1)
    if flide == 'book':
        cou = 1
    elif flide == 'author':
        cou = 2
    elif flide == 'publisher':
        cou = 3
    else:
        cou = 0
        
    context = {
        'x':'xxx',
        'cou': cou
    }
    return render(request,'insert.html',context)

def ibook(request):
    flide1 = request.POST.get('flide')
    id1 = request.POST.get("id")
    name = request.POST.get("name")
    page = request.POST.get("page")
    year = request.POST.get("year")
    publishern = request.POST.get("publishern")
    try:
        conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        sqlText = 'SELECT * From book1 LIMIT 5;'
        postgres_insert_query = """ INSERT INTO book (b_id, b_name, b_page,b_year, p_name) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = (str(id1), str(name), int(page), str(year), str(publishern))
        
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print (count, "Record inserted successfully into book table")
        messages.info(request, "Record inserted successfully into book table")
        return redirect('/query')

    except (Exception, psycopg2.Error) as error :
        if(conn):
            print("Failed to insert record into book table", error)
        messages.info(request,"Error")
        return redirect('/query')

    finally:
        #closing database connection.
        if(conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
    context = {
        'x':'xxx',
        'flide1': flide1
    }
    return render(request,'insert.html',context)

def iauthor(request):
    flide1 = request.POST.get('flide')
    name = request.POST.get("name")
    year = request.POST.get("year")
    try:
        conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        sqlText = 'SELECT * From book1 LIMIT 5;'
        postgres_insert_query = """ INSERT INTO author (a_name, a_year) VALUES (%s,%s)"""
        record_to_insert = ( str(name), str(year))
        
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print (count, "Record inserted successfully into author table")
        messages.info(request, "Record inserted successfully into author table")
        return redirect('/query')

    except (Exception, psycopg2.Error) as error :
        if(conn):
            print("Failed to insert record into author table", error)
        messages.info(request,"Error")
        return redirect('/query')

    finally:
        #closing database connection.
        if(conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def ipublisher(request):
    flide1 = request.POST.get('flide')
    name = request.POST.get("name")
    addr = request.POST.get("addr")
    try:
        conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
        conn.set_client_encoding('UTF8')
        cur = conn.cursor()
        sqlText = 'SELECT * From book1 LIMIT 5;'
        postgres_insert_query = """ INSERT INTO publisher (p_name, p_address) VALUES (%s,%s)"""
        record_to_insert = ( str(name), str(addr))
        
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        count = cur.rowcount
        print (count, "Record inserted successfully into publisher table")
        messages.info(request, "Record inserted successfully into publisher table")
        return redirect('/query')

    except (Exception, psycopg2.Error) as error :
        if(conn):
            print("Failed to insert record into publisher table", error)
        messages.info(request,"Error")
        return redirect('/query')

    finally:
        #closing database connection.
        if(conn):
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")

def qdele(request):
    id_del = request.POST.get('id1')
    id_colum = request.POST.get('id2')
    sql_text = str(request.POST.get('sql_text'))
    
    if id_colum == 'b_id':
        try:
            conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
            conn.set_client_encoding('UTF8')
            cur = conn.cursor()
            sql_delete_query = """Delete from book where b_id = %s"""
            cur.execute(sql_delete_query, (str(id_del), ))
            conn.commit()
            count = cur.rowcount
            print(count, "Record deleted successfully ")
            messages.info(request, "Record deleted successfully ")
            return redirect('/query')
        except (Exception, psycopg2.Error) as error:
            print("Error in Delete operation", error)
            messages.info(request, "Error in Delete operation")
            return redirect('/query')

        finally:
            # closing database connection.
            if (conn):
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                # messages.info(request, "PostgreSQL connection is closed")
                return redirect('/query')
    if id_colum == 'a_name':
        try:
            conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
            conn.set_client_encoding('UTF8')
            cur = conn.cursor()
            # Update single record now
            sql_delete_query = """Delete from author where a_name = %s"""
            cur.execute(sql_delete_query, (str(id_del), ))
            conn.commit()
            count = cur.rowcount
            print(count, "Record deleted successfully ")
            messages.info(request, "Record deleted successfully ")
            return redirect('/query')
        except (Exception, psycopg2.Error) as error:
            print("Error in Delete operation", error)
            messages.info(request, "Error in Delete operation")
            return redirect('/query')

        finally:
            # closing database connection.
            if (conn):
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                messages.info(request, "PostgreSQL connection is closed")
                return redirect('/query')
    if id_colum == 'p_name':
        try:
            conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
            conn.set_client_encoding('UTF8')
            cur = conn.cursor()
            # Update single record now
            sql_delete_query = """Delete from publisher where p_name = %s"""
            cur.execute(sql_delete_query, (str(id_del), ))
            conn.commit()
            count = cur.rowcount
            print(count, "Record deleted successfully ")
            messages.info(request, "Record deleted successfully ")
            return redirect('/query')

        except (Exception, psycopg2.Error) as error:
            print("Error in Delete operation", error)
            messages.info(request, "Error in Delete operation")
            return redirect('/query')

        finally:
            # closing database connection.
            if (conn):
                cur.close()
                conn.close()
                print("PostgreSQL connection is closed")
                # messages.info(request, "PostgreSQL connection is closed")
                return redirect('/query')


    messages.info(request, str(id_del)+str(id_colum))
    print(id_del)
    print(sql_text)
    return redirect('/query')
    
    # return render(request,'query.html')

def search(request):
    seach_book = str(request.POST.get('seach_book')).capitalize()
    seach_author = str(request.POST.get('seach_author')).capitalize()
    seach_publisher = str(request.POST.get('seach_publisher')).capitalize()
    
    num1 = str(request.POST.get('num1'))
    conn = psycopg2.connect(host="localhost",database="book1", user="postgres", password="123456")
    conn.set_client_encoding('UTF8')
    cur = conn.cursor() 
    if seach_book == '' or seach_book == "None":
        seach_book = ''
        sqbook = '%'
        cou = 1
    else:
        sqbook = seach_book + '%'
        cou = 1

    if seach_author == '' or seach_author == "None":
        seach_author= ''
        sqauthor = '%'
        cou = 1
    else:
        sqauthor = seach_author + '%'
        cou = 1

    if seach_publisher == '' or seach_publisher == "None":
        seach_publisher=''
        sqpublisher = '%'
        cou = 1
    else:
        sqpublisher = seach_publisher + '%'
        cou = 1

    if sqbook == '%' and sqauthor == '%' and sqpublisher == '%':
        limsql = 'limit 25 ;'
        cou = 0
    else:
        limsql = ' ;'
    # if seach_book == '' or seach_book == "None" and seach_author == '' or seach_author == "None" and seach_publisher == '' or seach_publisher == "None":
    #     cou = 0

    sqltext = """select book.b_name, work_for.a_name,    work_for.p_name from work_for 
    inner join write_for on work_for.a_name = write_for.a_name
    inner join book on write_for.b_id = book.b_id
    where book.b_name like """ + "'"+ sqbook +"'" + """ and work_for.a_name like """+ "'"+ sqauthor +"'" +  """  
    and work_for.p_name like """+ "'"+ sqpublisher +"' " +  limsql
    cur.execute(sqltext)    
    sql_list=cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    context = {
        'sql_list':sql_list,
        'colnames':colnames,
        'cou': cou,
        'seach_book':seach_book,
        'seach_author':seach_author,
        'seach_publisher':seach_publisher
    }
    print(sqbook)
    print(sqauthor)
    print(sqpublisher)
    return render(request,'seach.html',context)