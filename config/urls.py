from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "TAF-TYUTOR"
admin.site.site_title = "TAF-TYUTOR admin"
admin.site.index_title = "Boshqaruv paneli"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("students.urls")),
]
