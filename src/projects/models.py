from django.db import models
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string
from users.models import Users
import time




class Project(models.Model):
    project_name = models.CharField(max_length=200)
    user_id = models.ForeignKey(Users,on_delete=models.CASCADE)
    description = models.TextField()
    slug = models.CharField(max_length=500,unique=True)
    budget = models.FloatField(default=100.00)
    isClosed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self,*args,**kwargs):
        self.slug = unique_slugify(self.project_name)
        
        super(Project,self).save(*args,**kwargs)
    
    def __str__(self):
        return self.project_name
    
    

def unique_slugify(slug):
    unique_slug = slugify(slug + '-'+get_random_string(length=10,allowed_chars='abcdef0123456789_ '))
    while Project.objects.filter(slug=unique_slug).exists():
        unique_slug = slugify(slug + '-'+get_random_string(length=10,allowed_chars='abcdef0123456789_ '))
    return unique_slug



class Subscriber(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Users,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

   
