from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .symptoms_list import *
from .CNN_TESTING import get_result
import sqlite3


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html')
    else:
        username = request.POST['username'] 
        password1 = request.POST['password1'] 
        password2 = request.POST['password2'] 
        weight = request.POST['weight'] 
        height = request.POST['height'] 
        gender = request.POST['gender'] 
        BG = request.POST['BG'] 

            
        if (len(username)==0 or len(password1)==0 or len(password2)==0 or len(weight)==0 or len(height)==0):
            return render(request, 'todo/signupuser.html', {'error':'Consider all fields'})
        else:
            if(password1 == password2):
                try:
                    print('============ 1 ===================')
                    weight = int(weight)
                    height = int(height)
                    try:
                        print('============ 3 ===================')
                        user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                        user.save()
                        login(request, user)
                        print('============ 4 ===================')

                        BMI = ((weight / height) / height) * 10000
                        print('============ 5 ===================')

                        if BMI < 16:
                            category = "Severe Thinness"
                        elif BMI < 17:
                            category = "Moderate Thinness"
                        elif BMI < 18.5:
                            category = "Mild Thinness"
                        elif BMI < 25:
                            category = "Normal"
                        elif BMI < 30:
                            category = "Overweight"
                        elif BMI < 35:
                            category = "Obese Class 1"
                        elif BMI < 40:
                            category = "Obese Class 2"
                        else:
                            category = "Obese Class 3"
                        
                        print('============ 2 ===================')
                        con = sqlite3.connect("db.sqlite3")
                        cur = con.cursor()
                        sql = "INSERT INTO todo_registered_info ( name, weight, height, BG, M_F, BMI, category) VALUES (?,?,?,?,?,?,?)"
                        val = (username,weight,height,BG,gender,BMI,category)
                        cur.execute(sql, val)
                        con.commit()
                        print('============ 6 ===================')

                        f = open("current_user.txt", "w")
                        f.write(username)
                        f.close()
                        print('============ 7 ===================')

                        return render(request, 'todo/home.html', {'name':username, 'weight':weight, 'height':height, 'BG':BG, 'M_F':gender, 'BMI':BMI, 'category':category})

                    except IntegrityError:
                        return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new username'})
                except:
                    return render(request, 'todo/signupuser.html', {'error':'In place of weight and height please Enter numbers only'})
            else:
                return render(request, 'todo/signupuser.html', {'error':'Password did not matched'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            login(request, user)
            f = open("current_user.txt", "w")
            f.write(request.POST['username'])
            f.close()

            return redirect('currenttodos')



@login_required
def profile(request):
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    QP = []
    for data in cur.execute('SELECT * FROM todo_registered_info;'):
            QP.append(data)
    con.close()

    f = open("current_user.txt", "r")
    user_name = f.read()
    
    for index in range (0,len(QP)):
        if QP[index][1] == user_name:
            break

    username = QP[index][1]
    weight = QP[index][2]
    height= QP[index][3]
    BG = QP[index][4]
    gender = QP[index][5]
    BMI = QP[index][6]
    category = QP[index][7]

    return render(request, 'todo/profile.html', {'name':username, 'weight':weight, 'height':height, 'BG':BG, 'M_F':gender, 'BMI':BMI, 'category':category})


    # if request.method == 'POST':
        # logout(request)
        # return redirect('home')



@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})



@login_required
def predict_disease(request):
        return render(request, 'todo/predict_disease.html', {'form':TodoForm(),'symptoms':symptoms})


@login_required
def predicted_results(request):
    if request.method == 'GET':
        sym1 =request.GET['sys1']
        sym2 =request.GET['sys2']
        sym3 =request.GET['sys3']
        sym4 =request.GET['sys4']
        sym5 =request.GET['sys5']
        
        syms = [sym1,sym2,sym3,sym4,sym5]
        symptoms = []
        for sym in syms:
            if sym != 'none':
                symptoms.append(sym.replace('_',' '))
                
        symptoms_inserted = syms
        result,acc,doctor_info,exercise_info,diet_info,medicine_info = get_result(symptoms_inserted)
        print(result)
 
        return render(request, 'todo/predicted_result.html',{'form':TodoForm(),'symptoms':symptoms,'disease':result,'doctor':doctor_info,'excersize':exercise_info, 'accuracy':acc,'diet':diet_info ,'medicine':medicine_info})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
