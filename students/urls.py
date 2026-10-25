from django.urls import path

from . import views

app_name = "students"

urlpatterns = [
    path("", views.register, name="register"),
    path("success/", views.success, name="success"),
    path("passport/<int:pk>/", views.passport_file, name="passport_file"),
]
