from django.db import models

from users.models import Users

class Profile(models.Model):
    user_id = models.OneToOneField(Users,on_delete=models.CASCADE,unique=True)
    pro_picture = models.ImageField(null=True,upload_to='profile/')
    role = models.CharField(max_length=100,null=True)
    username = models.CharField(max_length=100,unique=True)
    bio = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return " "+self.username
