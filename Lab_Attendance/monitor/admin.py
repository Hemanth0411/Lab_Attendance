from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ('roll_no', 'first_name', 'last_name', 'dob', 'batch', 'year')
    search_fields = ('roll_no', 'first_name', 'last_name')

admin.site.register(Student, StudentAdmin)
