from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django import forms
from .models import *


class MyLoginView(LoginView):
    template_name = 'main/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')


def logout_view(request):
    logout(request)
    return redirect('login')


class RegisterView(FormView):
    template_name = 'main/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('task-list')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            
        return super(RegisterView, self).form_valid(form)
            

# Create your views here.
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "main/task_list.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        search_text = self.request.GET.get('search-text') or ''
        
        if search_text:
            context['tasks'] = context['tasks'].filter(title__icontains=search_text)
        
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "main/task_details.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    context_object_name = "task"
    template_name = "main/task_create.html"
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ("title", "description", "complete")
    context_object_name = "task"
    template_name = "main/task_update.html"
    success_url = reverse_lazy("task-list")

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'cols': 25,
        })
        return form


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "main/task_delete.html"
    success_url = reverse_lazy("task-list")