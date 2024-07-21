from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Student, Session, Computer, Department, Semester, Subject
from .forms import SubjectSelectionForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                student = Student.objects.get(user=user)
                if request.POST.get('subject'):  # If subject selection form submitted
                    subject_name = request.POST.get('subject')
                    subject = Subject.objects.get(name=subject_name)
                    computer = Computer.objects.filter(status='available').first()
                    session = Session(student=student, computer=computer, subject=subject.name, current_semester=student.semester)
                    computer.status = 'in use'
                    computer.save()
                    session.save()
                    return redirect('student_dashboard')
                else:
                    form = SubjectSelectionForm()
                    return render(request, 'select_subject.html', {'form': form})
            except Student.DoesNotExist:
                return render(request, 'login.html', {'error': 'Student not found'})
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'login.html')

@login_required
def student_dashboard(request):
    student = request.user.student
    sessions = Session.objects.filter(student=student)
    return render(request, 'student_dashboard.html', {'sessions': sessions})

@login_required
def admin_dashboard(request):
    sessions = Session.objects.all()
    return render(request, 'admin_dashboard.html', {'sessions': sessions})

def logout_view(request):
    logout(request)
    return redirect('login')
