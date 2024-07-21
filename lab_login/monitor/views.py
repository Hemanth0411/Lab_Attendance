from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import StudentForm
from .models import Student
from django.forms import modelformset_factory

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def add_students(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_students.html', {'form': form})

def edit_student(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'edit_student.html', {'form': form})

def delete_student(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    student.delete()
    return redirect('student_list')

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


