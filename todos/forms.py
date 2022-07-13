from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import model_to_dict

from todolist.validator import dash_validator
from todos.models import Todo


class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
    file = forms.FileField(required=False)


class NewTodoForm(forms.Form):
    tagged_users = forms.MultipleChoiceField(
        choices=[(u.id, u.username) for u in User.objects.all() if len(u.username) == 1],
        widget=forms.CheckboxSelectMultiple
    )
    # tagged_users = forms.ModelMultipleChoiceField(
    #     queryset=User.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    title = forms.CharField(max_length=200, validators=[dash_validator])
    description = forms.CharField(required=False)
    completed = forms.BooleanField(required=False)

    def __init__(self, instance=None, initial=None, *args, **kw):
        super().__init__(*args, **kw)
        self.instance = instance
        if instance:
            todo_data = model_to_dict(instance)
        else:
            todo_data = {}
        if initial:
            todo_data.update(initial)
        if instance:
            todo_data['tagged_users'] = [u.id for u in self.instance.tagged_users.all()]
        self.initial = todo_data

    def clean_tagged_users(self):
        d = self.cleaned_data
        users = User.objects.filter(id__in=d['tagged_users'])
        return users

    def save(self, todo):
        d = self.cleaned_data
        todo.tagged_users.add(*d['tagged_users'])
        todo.title = d['title']
        todo.description = d['description']
        todo.save()


class TodoForm(forms.ModelForm):
    pass

    class Meta:
        model = Todo
        exclude = ['owner', 'completed', 'completed_on']


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=150)

    def save(self):
        d = self.cleaned_data
        user = authenticate(
            username=d['username'],
            password=d['password']
        )
        return user


class RegisterForm(forms.Form):
    email = forms.EmailField(label='email')
    username = forms.CharField(label='username', max_length=150)
    password = forms.CharField(label='password', max_length=150)

    def create(self):
        d = self.cleaned_data
        user = User.objects.create_user(
            email=d['email'],
            username=d['username'],
            password=d['password']
        )
        return user
