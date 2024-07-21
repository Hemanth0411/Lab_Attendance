from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.text import slugify
from .models import Department, Semester, Subject, Student, Computer, Session

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'section', 'semester', 'batch', 'department', 'birth_date')

    def save_model(self, request, obj, form, change):
        if not change:  # Only on creation, not on update
            username = obj.roll_no
            birth_date = obj.birth_date
            password = f"{birth_date.day:02}{birth_date.month:02}{slugify(obj.name[:4]).lower()}"
            user = User(username=username, password=make_password(password))
            user.save()
            obj.user = user
        super().save_model(request, obj, form, change)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'computer', 'start_time', 'end_time', 'subject')
    search_fields = ('student__roll_no', 'student__name', 'student__batch', 'student__department__name', 'subject')

admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Student, StudentAdmin)
admin.site.register(Computer)
admin.site.register(Session, SessionAdmin)
