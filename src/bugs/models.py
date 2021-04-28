from django.db import models
from django.db.models import CASCADE
from users.models import Users
from projects.models import Project,Subscriber
from tasks.models import Task


class Bug(models.Model):
    project = models.ForeignKey(Project,on_delete=CASCADE)
    task = models.ForeignKey(Task,on_delete=CASCADE)
    registered_by = models.ForeignKey(Users,on_delete=CASCADE)

    name = models.CharField(max_length=400)
    description = models.TextField()
    reproduce = models.TextField(null=True)


    is_close =  models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)




