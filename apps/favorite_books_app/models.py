from django.db import models
import re
import bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validaciones_basicas(self, postData):
        errores = {}

        if len (postData['first_name'])<2:
            errores['first_name']= "Nombre debe tener al menos 2 caracteres"
        if len (postData['last_name'])<2:
            errores['last_name']= "Apellido debe tener al menos 2 caracteres"
        if len (postData['email']) <1:
            errores['email']= "Email es necesario"
        if len(postData['password']) < 5:
            errores['password']='Password debe tener al menos 5 caracteres'
        if postData['password'] != postData['confirmPassword']:
            errores['confirmacion'] = 'Contraseñas no coinciden'

        elif not EMAIL_REGEX.match(postData['email']):
            errores['email_not_valid']= "Email is not valid"

        else:
            user = User.objects.filter(email=postData['email'])
            if len(user)>0:
                errores['email_registered'] = 'Email ya registrado, porfavor intentar otro email'

        return errores

    def login_validaciones(self, postData):
        login_errores = {}

        if len(postData['email']) < 1:
            login_errores['email'] = 'Email es necesario'
        elif not EMAIL_REGEX.match(postData['email']):
            login_errores['email']= "Email is not valid"
        else:
            email_existente = User.objects.filter(email=postData['email'])
            if len(email_existente) == 0:
                login_errores['email_no_encontrado'] = 'Este correo no está registrado'
                return login_errores
            else:
                user = email_existente[0]
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                login_errores['password']='Password incorrecta'
            
        return login_errores

class BookManager(models.Manager):
    def book_validations(self, postData):
        book_errors = {}

        if 'title' in postData and len(postData['title']) == 0:
            book_errors['title'] = 'Title is required'
        if len(postData['desc']) < 5:
            book_errors['desc'] = 'Description must be at least 5 characters'
        
        return book_errors
    
    

class Book(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='books_uploaded')
    users_who_like = models.ManyToManyField('User', related_name='liked_books')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = BookManager()

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
