import uuid
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models

# Pasport fayllari MEDIA_ROOT dan TASHQARIDA saqlanadi — to'g'ridan-to'g'ri URL orqali ochilmaydi.
private_storage = FileSystemStorage(location=settings.PRIVATE_MEDIA_ROOT)

MAX_PASSPORT_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file_size(f):
    if f.size > MAX_PASSPORT_SIZE:
        raise ValidationError("Fayl hajmi 5 MB dan oshmasligi kerak.")


def passport_upload_to(instance, filename):
    # Asl fayl nomi saqlanmaydi — tasodifiy nom beriladi
    ext = Path(filename).suffix.lower()
    return f"passports/{uuid.uuid4().hex}{ext}"


class Group(models.Model):
    """Guruhlar admin panelda qo'shiladi. Formada kurs tanlansa, faqat o'sha kurs guruhlari chiqadi."""
    COURSE_CHOICES = [(i, f"{i}-kurs") for i in range(1, 5)]

    name = models.CharField("Guruh nomi", max_length=50)
    course = models.PositiveSmallIntegerField("Kurs", choices=COURSE_CHOICES)

    class Meta:
        verbose_name = "Guruh"
        verbose_name_plural = "Guruhlar"
        ordering = ["course", "name"]
        unique_together = ("name", "course")

    def __str__(self):
        return f"{self.name} ({self.course}-kurs)"


class Student(models.Model):
    class Residence(models.TextChoices):
        IJARA = "ijara", "Ijara"
        TTJ = "ttj", "TTJ"
        QARINDOSH = "qarindosh", "Yaqin qarindosh"
        OZ_UYI = "oz_uyi", "O'zining uyi"

    course = models.PositiveSmallIntegerField("Kurs", choices=Group.COURSE_CHOICES)
    group = models.ForeignKey(Group, on_delete=models.PROTECT, verbose_name="Guruh", related_name="students")
    last_name = models.CharField("Familiya", max_length=100)
    first_name = models.CharField("Ism", max_length=100)
    middle_name = models.CharField("Otasining ismi", max_length=100, default="")
    residence_type = models.CharField("Yashash joyi", max_length=20, choices=Residence.choices)
    current_address = models.CharField("Hozirgi yashash manzili", max_length=255)
    # Talaba xaritada o'zi belgilaydi (ixtiyoriy) — tyutor uyga borganda manzilni topish uchun
    latitude = models.DecimalField("Kenglik", max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField("Uzunlik", max_digits=9, decimal_places=6, null=True, blank=True)
    passport_file = models.FileField(
        "Pasport nusxasi",
        storage=private_storage,
        upload_to=passport_upload_to,
        validators=[FileExtensionValidator(["jpg", "jpeg", "png", "pdf"]), validate_file_size],
    )
    created_at = models.DateTimeField("Ro'yxatdan o'tgan vaqt", auto_now_add=True)

    class Meta:
        verbose_name = "Talaba"
        verbose_name_plural = "Talabalar"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def has_location(self):
        return self.latitude is not None and self.longitude is not None

    def delete(self, *args, **kwargs):
        # Talaba o'chirilsa, pasport fayli ham diskdan o'chadi
        storage, name = self.passport_file.storage, self.passport_file.name
        super().delete(*args, **kwargs)
        if name:
            storage.delete(name)
