from django import forms

from .models import Group, Student

# Fayl ichidagi haqiqiy turini tekshirish uchun "magic bytes"
FILE_SIGNATURES = {
    b"\xff\xd8\xff": "jpg",
    b"\x89PNG\r\n\x1a\n": "png",
    b"%PDF": "pdf",
}


class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            "course", "group", "last_name", "first_name", "middle_name",
            "residence_type", "current_address", "latitude", "longitude", "passport_file",
        ]
        widgets = {
            "latitude": forms.HiddenInput,
            "longitude": forms.HiddenInput,
            "residence_type": forms.RadioSelect,
            "current_address": forms.TextInput(
                attrs={"placeholder": "Masalan: Chilonzor tumani, 9-kvartal, 12-uy"}
            ),
            "passport_file": forms.ClearableFileInput(attrs={"accept": ".jpg,.jpeg,.png,.pdf"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["course"].choices = [("", "— Kursni tanlang —")] + Group.COURSE_CHOICES
        self.fields["group"].empty_label = "— Guruhni tanlang —"
        # RadioSelect da bo'sh "Select an option" varianti chiqmasligi uchun
        self.fields["residence_type"].choices = Student.Residence.choices

        required_msgs = {
            "course": "Kursni tanlang.",
            "group": "Guruhni tanlang.",
            "last_name": "Familiyani kiriting.",
            "first_name": "Ismni kiriting.",
            "middle_name": "Otasining ismini kiriting.",
            "residence_type": "Yashash joyini tanlang.",
            "current_address": "Hozirgi manzilni kiriting.",
            "passport_file": "Pasport nusxasini yuklang.",
        }
        for name, msg in required_msgs.items():
            self.fields[name].error_messages["required"] = msg

    def clean_passport_file(self):
        f = self.cleaned_data.get("passport_file")
        if f:
            head = f.read(8)
            f.seek(0)
            if not any(head.startswith(sig) for sig in FILE_SIGNATURES):
                raise forms.ValidationError("Fayl JPG, PNG yoki PDF bo'lishi kerak.")
        return f

    def clean(self):
        data = super().clean()
        group, course = data.get("group"), data.get("course")
        if group and course and group.course != course:
            self.add_error("group", "Bu guruh tanlangan kursga tegishli emas.")

        # Lokatsiya ixtiyoriy: ikkalasi ham bo'lsa va to'g'ri bo'lsa saqlanadi, aks holda tashlab yuboriladi
        lat, lon = data.get("latitude"), data.get("longitude")
        if lat is None or lon is None or not (-90 <= lat <= 90 and -180 <= lon <= 180):
            data["latitude"] = data["longitude"] = None
        return data
