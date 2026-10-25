import mimetypes
from pathlib import Path

from django.contrib.admin.views.decorators import staff_member_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StudentRegisterForm
from .models import Group, Student


def register(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("students:success")
    else:
        form = StudentRegisterForm()

    groups = list(Group.objects.values("id", "name", "course"))
    return render(request, "students/register.html", {"form": form, "groups": groups})


def success(request):
    return render(request, "students/success.html")


@staff_member_required
def passport_file(request, pk):
    """Pasport faylini faqat admin/staff login qilgan foydalanuvchi ochadi."""
    student = get_object_or_404(Student, pk=pk)
    if not student.passport_file:
        raise Http404
    name = student.passport_file.name
    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    response = FileResponse(student.passport_file.open("rb"), content_type=content_type)
    response["Content-Disposition"] = f'inline; filename="pasport_{student.pk}{Path(name).suffix}"'
    response["X-Content-Type-Options"] = "nosniff"
    response["Cache-Control"] = "private, no-store"
    return response
