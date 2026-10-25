from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html

from .export import xlsx_response
from .models import Group, Student


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ("name", "course", "student_count")
    list_filter = ("course",)
    search_fields = ("name",)

    @admin.display(description="Talabalar soni")
    def student_count(self, obj):
        return obj.students.count()


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    change_list_template = "admin/students/student/change_list.html"
    actions = ["export_selected_xlsx"]
    list_display = (
        "last_name", "first_name", "middle_name", "course", "group",
        "residence_type", "current_address", "map_links", "passport_link", "created_at",
    )
    list_filter = ("course", "group", "residence_type")
    search_fields = ("last_name", "first_name", "middle_name", "group__name", "current_address")
    list_select_related = ("group",)
    readonly_fields = ("map_links", "passport_link", "created_at")
    fieldsets = (
        ("Talaba", {"fields": ("course", "group", "last_name", "first_name", "middle_name")}),
        ("Yashash joyi", {"fields": ("residence_type", "current_address", "latitude", "longitude", "map_links")}),
        # passport_file maydoni ataylab ko'rsatilmaydi: Django uning yonida ochiq MEDIA_URL
        # havolasini chiqaradi. Fayl faqat himoyalangan "Ko'rish" havolasi orqali ochiladi.
        ("Hujjat", {"fields": ("passport_link",)}),
        ("Tizim", {"fields": ("created_at",)}),
    )

    @admin.display(description="Xaritada")
    def map_links(self, obj):
        if not obj.has_location:
            return "—"
        lat, lon = obj.latitude, obj.longitude
        return format_html(
            '<a href="https://yandex.uz/maps/?rtext=~{},{}&rtt=auto" target="_blank">Yandex</a> · '
            '<a href="https://www.google.com/maps/dir/?api=1&destination={},{}" target="_blank">Google</a>',
            lat, lon, lat, lon,
        )

    @admin.display(description="Pasport")
    def passport_link(self, obj):
        if not obj.pk or not obj.passport_file:
            return "—"
        url = reverse("students:passport_file", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">Ko\'rish</a>', url)

    # --- Excel eksport ---
    @admin.action(description="Tanlanganlarni Excelga yuklab olish")
    def export_selected_xlsx(self, request, queryset):
        return xlsx_response(queryset)

    def get_urls(self):
        custom = [
            path("export-xlsx/", self.admin_site.admin_view(self.export_filtered_xlsx),
                 name="students_student_export_xlsx"),
        ]
        return custom + super().get_urls()

    def export_filtered_xlsx(self, request):
        """Ro'yxatdagi joriy filtr va qidiruvga mos barcha talabalarni eksport qiladi."""
        cl = self.get_changelist_instance(request)
        return xlsx_response(cl.get_queryset(request))
