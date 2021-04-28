from django.shortcuts import render,redirect,Http404
from django.core.exceptions import ValidationError
from tasks.views import get_projects_from_slug,get_user_from_id,return_alert_message
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Sum
from users.models import Users
from projects.models import Project,Subscriber
from .forms import ExpenseCreationForm
from .models import Expense,get_total_expense

__path = 'views/expenses/'
templates = {
    'create':__path+'create_expense.html',
    'list':__path+'list_expenses.html',
    'details':__path+'expense_details.html',
    'update':__path+'update_expenses.html'
}



@login_required
def create_expense(request,slug):
    user = request.user
    context = {}
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    project = projects[0]
    

    if request.method == 'POST':
        expenseForm = ExpenseCreationForm(request.POST)
        if expenseForm.is_valid():
            name = expenseForm.cleaned_data['name']
            description = expenseForm.cleaned_data['description']
            expense = expenseForm.cleaned_data['expense']
            try:
                newExpense = Expense(project=project,registered_by=user,name=name,description=description,expense=expense)
                newExpense.save()
                return redirect('project_details',slug=slug)
            except ValidationError as e:
                context['errors'] = e.message
        else:
            context['errors']=expenseForm.errors
    context['project'] = project
    get_total_expense(project,context)
    return render(request,templates['create'],context=context)


@login_required
def expense_details(request,slug,id):
    user = request.user
    context = {}
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    project = projects[0]
    expense = None
    try:
        expense = Expense.objects.get(pk=id,project=project)
    except Expense.DoesNotExist:
        raise Http404()
    
    context['expense'] = expense
    context['project'] = project

    get_total_expense(project,context)

    return render(request,templates.get('details'),context=context)


@login_required
def edit_details(request,slug,id):
    print(request)
    user = request.user
    context = {}
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    project = projects[0]
    expense = None
    try:
        expense = Expense.objects.get(pk=id,project=project)
    except Expense.DoesNotExist:
        raise Http404()
    
    if expense.registered_by != user:
        raise Http404()

    if request.method != 'POST':
        return redirect('expense_details',slug=slug,id=id)
    
    context['expense'] = expense
    context['project'] = project

    expenseForm = ExpenseCreationForm(request.POST)
    if expenseForm.is_valid():
        name = expenseForm.cleaned_data['name']
        description = expenseForm.cleaned_data['description']
        expenses = expenseForm.cleaned_data['expense']
        
        expense.name= name
        expense.description = description
        expense.expense = expenses
        try:
            expense.save()
            return redirect('expense_details',slug=slug,id=id)
        except ValidationError as e:
            context['errors']= e.message

        
    else:
        print("Hello World")
        print(expenseForm.errors)
        context['errors'] = expenseForm.errors

    get_total_expense(project,context)
    print(context)
    return render(request,templates.get('details'),context=context)


@login_required
def delete_expense(request,slug,id):
    user = request.user
    context = {}
    projects = get_projects_from_slug(slug).filter(Q(subscriber__subscriber=user)|Q(user_id=user))
    if not projects.exists():
        raise Http404()
    
    project = projects[0]
    expense = None
    try:
        expense = Expense.objects.get(pk=id,project=project)
    except Expense.DoesNotExist:
        raise Http404()
    
    if expense.registered_by != user:
        raise Http404()

    if request.method != 'POST':
        return redirect('expense_details',slug=slug,id=id)
    
    expense.delete()

    return redirect('project_details',slug=slug)