from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentForm, AttendanceForm, YearBatchForm
from .models import Student, Subject, Attendance
import logging
from django.contrib import messages

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
        year = request.POST.get('year')
        form = StudentForm(request.POST, year=year)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        year = request.GET.get('year', None)
        form = StudentForm(year=year)
    return render(request, 'add_students.html', {'form': form})

def edit_student(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student, year=student.year)
    return render(request, 'edit_student.html', {'form': form})

def student_list(request):
    year = request.GET.get('year')
    batch = request.GET.get('batch')
    
    students = Student.objects.all().order_by('roll_no')
    
    if year:
        students = students.filter(year=year)
    if batch:
        students = students.filter(batch=batch)

    return render(request, 'student_list.html', {'students': students})

def delete_student(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    student.delete()
    return redirect('student_list')


logger = logging.getLogger(__name__)

"""def record_attendance(request):
    year_batch_form = YearBatchForm()
    students = None
    attendance_form = AttendanceForm()

    if request.method == 'POST':
        if 'filter_students' in request.POST:
            year_batch_form = YearBatchForm(request.POST)
            if year_batch_form.is_valid():
                year = year_batch_form.cleaned_data['year']
                batch = year_batch_form.cleaned_data['batch']
                students = Student.objects.filter(year=year, batch=batch)
                attendance_form = AttendanceForm(students=students)
        elif 'submit_attendance' in request.POST:
            attendance_form = AttendanceForm(request.POST)
            if attendance_form.is_valid():
                subject = attendance_form.cleaned_data['subject']
                student_ids = request.POST.getlist('students')
                for student_id in student_ids:
                    student = Student.objects.get(id=student_id)
                    Attendance.objects.create(student=student, subject=subject)
                    if subject.name == 'C-Language':
                        student.c_language_attendance += 1
                    elif subject.name == 'IT':
                        student.it_attendance += 1
                    elif subject.name == 'DS':
                        student.ds_attendance += 1
                    elif subject.name == 'OS':
                        student.os_attendance += 1
                    elif subject.name == 'Java':
                        student.java_attendance += 1
                    elif subject.name == 'DBMS':
                        student.dbms_attendance += 1
                    elif subject.name == 'Python':
                        student.python_attendance += 1
                    elif subject.name == 'WT':
                        student.wt_attendance += 1
                    elif subject.name == 'R':
                        student.r_attendance += 1
                    elif subject.name == 'CD':
                        student.cd_attendance += 1
                    student.save()
                return redirect('attendance_success')

    return render(request, 'record_attendance.html', {
        'year_batch_form': year_batch_form,
        'attendance_form': attendance_form,
        'students': students,
    })"""

logger = logging.getLogger(__name__)

def record_attendance(request):
    year_batch_form = YearBatchForm()
    students = None
    attendance_form = AttendanceForm()

    if request.method == 'POST':
        if 'filter_students' in request.POST:
            year_batch_form = YearBatchForm(request.POST)
            if year_batch_form.is_valid():
                year = year_batch_form.cleaned_data['year']
                batch = year_batch_form.cleaned_data['batch']
                students = Student.objects.filter(year=year, batch=batch)
                attendance_form = AttendanceForm(students=students)
        elif 'submit_attendance' in request.POST:
            year = request.POST.get('year')
            batch = request.POST.get('batch')
            students = Student.objects.filter(year=year, batch=batch)
            attendance_form = AttendanceForm(request.POST, students=students)
            if attendance_form.is_valid():
                subject = attendance_form.cleaned_data['subject']
                selected_roll_nos = attendance_form.cleaned_data['students']
                selected_students = Student.objects.filter(roll_no__in=selected_roll_nos)
                for student in selected_students:
                    Attendance.objects.create(student=student, subject=subject)
                    if subject.name == 'C-Language':
                        student.c_language_attendance += 1
                    elif subject.name == 'IT':
                        student.it_attendance += 1
                    elif subject.name == 'DS':
                        student.ds_attendance += 1
                    elif subject.name == 'OS':
                        student.os_attendance += 1
                    elif subject.name == 'Java':
                        student.java_attendance += 1
                    elif subject.name == 'DBMS':
                        student.dbms_attendance += 1
                    elif subject.name == 'Python':
                        student.python_attendance += 1
                    elif subject.name == 'WT':
                        student.wt_attendance += 1
                    elif subject.name == 'R':
                        student.r_attendance += 1
                    elif subject.name == 'CD':
                        student.cd_attendance += 1
                    student.save()
                logger.info("Attendance recorded successfully. Redirecting to success page.")
                return redirect('attendance_success')
            else:
                logger.error(f"Form errors: {attendance_form.errors}")

    return render(request, 'record_attendance.html', {
        'year_batch_form': year_batch_form,
        'attendance_form': attendance_form,
        'students': students,
    })


def attendance_summary(request):
    year_batch_form = YearBatchForm()
    attendance_data = []

    if request.method == 'POST':
        year_batch_form = YearBatchForm(request.POST)
        if year_batch_form.is_valid():
            year = year_batch_form.cleaned_data['year']
            batch = year_batch_form.cleaned_data['batch']
            students = Student.objects.filter(year=year, batch=batch)
            for student in students:
                subjects = {
                    'C_Language': student.c_language_attendance,
                    'IT': student.it_attendance,
                    'DS': student.ds_attendance,
                    'OS': student.os_attendance,
                    'Java': student.java_attendance,
                    'DBMS': student.dbms_attendance,
                    'Python': student.python_attendance,
                    'WT': student.wt_attendance,
                    'R': student.r_attendance,
                    'CD': student.cd_attendance,
                }
                attendance_data.append((student, subjects))
            return render(request, 'attendance_summary.html', {
                'year_batch_form': year_batch_form,
                'attendance_data': attendance_data,
            })
        else:
            logger.error(f"Form errors: {year_batch_form.errors}")
            messages.error(request, "There was an error in the form. Please try again.")

    return render(request, 'attendance_summary.html', {
        'year_batch_form': year_batch_form,
        'attendance_data': attendance_data,
    })

def attendance_success(request):
    return render(request, 'attendance_success.html')
