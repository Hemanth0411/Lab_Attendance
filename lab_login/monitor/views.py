from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from .forms import StudentFormSet
from .models import Student

def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                return HttpResponse("Invalid login credentials or not an admin.")
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def add_students(request):
    if request.method == 'POST':
        formset = StudentFormSet(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('student_list')
    else:
        formset = StudentFormSet(queryset=Student.objects.none())
    return render(request, 'add_students.html', {'formset': formset})

def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})
