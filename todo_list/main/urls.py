from django.urls import path
from .views import *


urlpatterns = [
    path('', TaskList.as_view(), name="task-list"),
    path('task-detail/<int:pk>/', TaskDetail.as_view(), name="task-details"),
    path('task-create/', TaskCreate.as_view(), name="task-create"),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name="task-update"),
    path('task-delete/<int:pk>/', TaskDelete.as_view(), name="task-delete"),
]