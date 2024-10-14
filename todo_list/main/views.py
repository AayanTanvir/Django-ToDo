from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import *
from django.urls import reverse_lazy
from django import forms

# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "main/task_list.html"


class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "main/task_details.html"


class TaskCreate(CreateView):
    model = Task
    fields = ('title', 'description',)
    context_object_name = "task"
    template_name = "main/task_create.html"
    success_url = reverse_lazy('task-list')

    def get_form(self, form_class = None):
        form = super().get_form(form_class)
        form.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'cols': 25,
        })
        return form


class TaskUpdate(UpdateView):
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


class TaskDelete(DeleteView):
    model = Task
    context_object_name = "task"
    template_name = "main/task_delete.html"
    success_url = reverse_lazy("task-list")