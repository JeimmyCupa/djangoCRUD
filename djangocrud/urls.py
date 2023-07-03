
from django.contrib import admin
from django.urls import path
from tasks import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("singup/",views.singup, name = "singup"),
    path("tasks/",views.tasks,name='tasks'),
    path("tasks_completed/",views.task_completed,name='tasks_completed'),
    path("logout/", views.singout, name="logout" ),
    path("singin/", views.singin, name="singin" ),
    path("tasks/create/", views.create_task, name="create_task" ),
    path("tasks/<int:task_id>/", views.task_detail, name= "task_detail"),
    path("tasks/<int:task_id>/complete",views.complete_task, name = 'complete_task'),
    path("tasks/<int:task_id>/delete",views.delete_task, name = 'delete_task')
]
