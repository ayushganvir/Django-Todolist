from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, HttpResponse
from django.views import View
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login as dlogin, logout
from todolist.file_handler import handle_uploaded_file
from .models import Todo
from .forms import TodoForm, RegisterForm, LoginForm, ContactForm, NewTodoForm
from datetime import date


def login(request):
    if request.POST:
        visitor = LoginForm(request.POST)
        if visitor.is_valid():
            user = visitor.save()
            if user is not None:
                dlogin(request, user)
                return HttpResponseRedirect(reverse('todo-index'))
            else:
                return HttpResponse("Wrong Credentials")
    return render(request, 'todos/login.html')


@require_GET
@login_required
def delete(request, todo_id):
    t = Todo.objects.get(id=todo_id)
    if request.user == t.owner:
        t.delete()
        return HttpResponseRedirect(reverse("todo-index"))
    else:
        return HttpResponse("You are not the owner")


@require_GET
@login_required
def completed(_request, todo_id):
    t = Todo.objects.get(id=todo_id)
    t.completed = not t.completed
    t.save()
    return HttpResponseRedirect(reverse("todo-index"))


@login_required
def index(request):
    print(request.user)
    todos = Todo.objects.filter(owner=request.user)
    users = [[u.email for u in t.tagged_users.all()] for t in todos]
    todo_zipped_list = zip(todos, users)
    # print(list(todo_zipped_list))
    if request.method == 'POST':
        tform = TodoForm(request.POST)
        if tform.is_valid():
            todo = tform.save(commit=False)
            todo.owner = request.user
            todo.save()
            return HttpResponseRedirect(reverse("todo-index",))
        else:
            print(tform.errors)
    else:
        today = date.today()
        d3 = today.strftime("%m/%d/%y")
        tform = TodoForm(initial={'title': '{}'.format(d3)})
    return render(request, 'todos/todo.html', {
        'tform': tform,
        'todo_zipped_list': todo_zipped_list,
    })


@require_GET
def title_detail(request, todo_id):
    t = Todo.objects.get(id=todo_id)
    context = {
        't': t,
    }
    return render(request, 'todos/todo_detail.html', context)


def t_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('todo-login'))


def register(request):
    print('IN REGISTER')
    if request.POST:
        print(request.POST)
        v = RegisterForm(request.POST)
        if v.is_valid():
            print(v)
            v.create()
            return HttpResponseRedirect(reverse('todo-login'))

    return render(request, 'todos/register.html')


def contact_me(request):
    if request.POST:
        print('in contact me')
        form = ContactForm(request.POST, request.FILES)
        print('form is >>>', request.FILES)

        if form.is_valid():
            print('in form valid')
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            handle_uploaded_file(request.FILES['file'])

            print('form is >>>', request.FILES)

            recipients = ['ayushganvir143@gmail.com']
            if cc_myself:
                recipients.append(sender)
            send_mail(subject, message, sender, recipients
                    )
            return HttpResponseRedirect(reverse('todo-index'))
        else:
            print(form.errors)
    else:
        form = ContactForm()
    return render(request, 'todos/contact_me.html', context= {'form': form})


class EditTodo(View):

    def post(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        form = NewTodoForm(request.POST)
        if form.is_valid():
            form.save(todo)
        return HttpResponseRedirect(reverse('todo-index'))

    def get(self, request, todo_id):
        todo = Todo.objects.get(id=todo_id)
        form = NewTodoForm(todo, initial={'title': todo.title.upper()})
        # from IPython import embed; embed()
        return render(request, 'todos/edit_todo.html', context={'form': form, 'todo': todo})




