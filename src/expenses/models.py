from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from users.models import Users  
from projects.models import Project,Subscriber

def get_total_expense(project,context=None):
    temp = Expense.objects.filter(project=project).aggregate(ue = Sum('expense'))['ue']
    val =0 if temp is None else temp
    if context is not None:
        context['leftover'] = project.budget-val
        print(context['leftover'])
        if context.get('leftover') > 0.5*project.budget:
            context['status']='success'
        elif (context.get('leftover') <=0.5*project.budget) and (context.get('leftover') >0.25*project.budget):
            context['status']='warning'
        else:
            context['status']='danger'
        

    else:
        return val
    


class Expense(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE)
    registered_by = models.ForeignKey(Users,on_delete=models.SET_NULL,null=True)
    name    = models.CharField(max_length=300)
    description = models.TextField()
    expense = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


    def save(self,*args,**kwargs):
        if self.registered_by is not None:
            if (not Subscriber.objects.filter(project=self.project,subscriber=self.registered_by).exists()) and (self.project.user_id != self.registered_by )  :
                raise ValidationError('User is not subscribed to this project')
       
        sum_of_expenses = get_total_expense(self.project)
        max_expense = self.project.budget

        if sum_of_expenses >=max_expense :
            raise ValidationError('Already Maxium Expense Reached For the Project')
            
        if self.expense>max_expense:
            raise ValidationError('Expenses Must be less than Budget of the Project')

        if self.expense<1:
            raise ValidationError('Expenses Must be more than 0')
        
        super(Expense,self).save(*args,**kwargs)

    
    @property
    def sum_of_expenses(self):
        return self.objects.filter(project=self.project).aggregate(sum_of_expenses=models.Sum('expense'))['sum_of_expenses']
    

    def __str__(self):
        return self.name