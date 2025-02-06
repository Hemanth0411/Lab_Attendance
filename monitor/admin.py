from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'name', 'batch', 'year')
    search_fields = ('roll_no', 'name')

admin.site.register(Student, StudentAdmin)
