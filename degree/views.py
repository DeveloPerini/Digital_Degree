from django.shortcuts import render , redirect
from . models import Student
from . forms import StudentForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
import random
import json
import hashlib
from web3 import Web3
import redis

def home(request):
    return render(request , 'degree/Home.html')


def SignIn(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'degree/Signin.html', {'form': form})    




def Login(request):
  warning = None
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    if user is not None:
      login(request, user)
      if user.is_staff:  
        last_ip = r.get(f'{user.username}:last_ip')
        current_ip = request.META['REMOTE_ADDR']
        if last_ip is not None and last_ip != current_ip:
          warning = 'Il tuo ultimo accesso è stato effettuato da un indirizzo IP diverso. Assicurati che questo sia il tuo accesso!'
        else:
          warning = None
        r.set(f'{user.username}:last_ip', current_ip)   
        return render(request , 'degree/add_student.html' , {'warning': warning})
      else:  
        return redirect('search')  
    else:
      return render(request, 'degree/Login.html', {'error': 'Invalid username or password'})
  else:
    return render(request, 'degree/Login.html',)




def search(request):
    return render(request , 'degree/search.html')


def student_details(request):
    identifier = request.GET.get('identifier')
    if not identifier:
        messages.error(request, 'Devi fornire un identificativo per cercare lo studente')
        return redirect('search')
    try:
        student = Student.objects.get(identifier=identifier)
    except Student.DoesNotExist:
        messages.error(request, 'Lo studente non è stato trovato')
        return redirect('search')
    return render(request, 'degree/student_details.html', {'student': student})      


def student_list(request):
    students = Student.objects.all()
    return render(request, 'degree/student_list.html', {'students': students})


def is_admin(user):
  return user.is_staff    

@user_passes_test(is_admin)
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            surname = form.cleaned_data['surname']
            birth_date = form.cleaned_data['birth_date']
            graduation_date = form.cleaned_data['graduation_date']
            grade = form.cleaned_data['grade']
            degree = form.cleaned_data['degree']
            
            w3 = Web3(Web3.HTTPProvider('https://goerli.infura.io/v3/c6a5a2106678423da4da073723891fc5'))
            privateKey = '93c699f6bd96af184c49112ad9876bd469e600603b4351de6cf983fd82a5b782'
            address = '0x71d574755824C7A7100714791cb542C8157E8cF0'
            nonce = w3.eth.getTransactionCount(address)
            gasPrice = w3.eth.gasPrice
            value = w3.toWei(0, 'ether')
            signedTx = w3.eth.account.signTransaction(dict(
                nonce = nonce,
                gasPrice = gasPrice,
                gas = 100000,
                to = '0x0000000000000000000000000000000000000000',
                value = value,
                data= hashlib.sha256(json.dumps({
                    'student': {
                        'name': name,
                        'surname': surname,
                        'date_of_birth': birth_date.strftime('%Y-%m-%d'),
                        'graduation_date': graduation_date.strftime('%Y-%m-%d'),
                        'grade': grade,
                        'degree': degree,
                    },
                }).encode('utf-8')).hexdigest()
            ), privateKey)

            tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
            txId = w3.toHex(tx)

            characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            identifier = ''
            for i in range(10):
                identifier += random.choice(characters)

            student = Student(name=name, surname=surname, birth_date=birth_date, graduation_date=graduation_date, grade=grade, degree=degree,)
            student.txId = txId
            student.identifier = identifier
            student.save()
            
            return redirect('student_list')
    else:
        form = StudentForm()
    
    return render(request, 'degree/add_student.html', {'form': form})


def logout_view(request):
  logout(request)  
  return redirect('login')      








