from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.core.exceptions import PermissionDenied



def index(request):
    return render(request, 'login.html')

def register(request):
    if request.method =='POST':
        errores = User.objects.validaciones_basicas(request.POST)
        if len(errores) > 0:
            for key, value in errores.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
            newuser = User.objects.create(
                first_name=request.POST['first_name'],
                last_name= request.POST['last_name'],
                email= request.POST['email'],
                password= hash1)
            newuser.id = request.session['id']
        return redirect('/books')

def login(request):
    if request.method =='POST':
        login_validator = User.objects.login_validaciones(request.POST)
        if len(login_validator)>0:
            for key, value in login_validator.items():
                messages.error(request, value)
            return redirect('/')
        user = User.objects.filter(email=request.POST['email'])[0]
        request.session['id'] = user.id
        return redirect('/books')
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')


def success(request):
    if 'id' not in request.session:
        return redirect('/')
    if request.method == 'GET':
        books =  Book.objects.all()
        context = {
            'books' : books,
            'user' : User.objects.get(id=request.session['id'])
        }
        return render(request, 'books.html', context)
    elif request.method == 'POST':
        books_validation = Book.objects.book_validations(request.POST)
        if len(books_validation)>0:
            for key, value in books_validation.items():
                messages.error(request, value)
            return redirect('/books')
            
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.create(
            title = request.POST['title'],
            desc = request.POST['desc'],
            uploaded_by = user,
        )
        book.users_who_like.add(user)
        book.save()
    return redirect('/books')

def edit(request, id_book):
    book_to_edit = Book.objects.get(id=id_book)
    user = User.objects.get(id=request.session['id'])
    if request.method == 'GET':
        context = {
            'book' : book_to_edit,
            'user': user
        }
        return render(request, 'book_uploaded.html', context)

    if request.method == 'POST':
        errores = Book.objects.book_validations(request.POST)
        if len(errores)>0:
            for key, value in errores.items():
                messages.error(request, value)
            # context = {
            #     'errores':errores,
            #     'user' : User.objects.get(id=request.session['id'])
            # }
            return redirect(f'/books/{book_to_edit.id}')
        book_to_edit.desc = request.POST['desc']
        book_to_edit.save()
        return redirect('/books')


def delete(request, id_book):
    book = Book.objects.get(id=id_book)
    if book.uploaded_by.id != request.session['id']:
        raise PermissionDenied
    book.delete()
    return redirect('/books')

def favorite(request, id_book):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.get(id=id_book)
        user.liked_books.add(book)
    return redirect(f'/books/{book.id}')


def unfavorite(request, id_book):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        book = Book.objects.get(id=id_book)
        user.liked_books.remove(book)
    return redirect(f'/books/{book.id}')
