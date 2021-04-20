from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

import datetime


class UserManger(BaseUserManager):
    def create_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError('user must have an email')
        
        if not first_name:
            raise ValueError('user must have a first name')
        
        if not last_name:
            raise ValueError('user must have a last name')
        
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    

    def create_superuser(self,email,first_name,last_name,password=None):
        user = self.create_user(email,first_name,last_name,password)

        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user



class Users(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login =  models.DateTimeField(auto_created=True,null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    objects = UserManger()
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        return self.first_name+' '+self.last_name
    
    def get_short_name(self):
        return self.first_name

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True

    
    



# Create your models here.
