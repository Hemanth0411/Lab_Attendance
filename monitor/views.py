from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import StudentForm, AttendanceForm, YearBatchForm, SessionFilterForm, ImportStudentsForm, PartFilter, \
    UploadSessionsForm, ReduceAttendanceForm
from .models import Student, Subject, Attendance, Session
import logging
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


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
                form.add_error(None, 'Invalid username or password')
        else:
            print(form.errors)
    else:
        form = AuthenticationForm()

    return render(request, 'admin_login.html', {'form': form})


def admin_logout(request):
    logout(request)
    return redirect('admin_login')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')


@login_required
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


@login_required
def import_students(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        form = ImportStudentsForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file, engine='openpyxl')

            for _, row in df.iterrows():
                roll_no = row['roll_no']
                name = row['name']
                year = row['year']
                batch = row['batch']
                if not Student.objects.filter(roll_no=roll_no).exists():
                    Student.objects.create(
                        roll_no=roll_no,
                        name=name,
                        year=year,
                        batch=batch
                    )
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=400)
    return render(request, 'import_students.html', {'form': ImportStudentsForm()})


@login_required
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


@login_required
def student_list(request):
    year = request.GET.get('year')
    batch = request.GET.get('batch')

    students = Student.objects.all().order_by('roll_no')

    if year:
        students = students.filter(year=year)
    if batch:
        students = students.filter(batch=batch)

    return render(request, 'student_list.html', {'students': students})


@login_required
def clear_student_records(request):
    if request.method == 'POST':
        year = request.POST.get('year')
        batch = request.POST.get('batch')

        students_to_delete = Student.objects.all()

        if year:
            students_to_delete = students_to_delete.filter(year=year)
        if batch:
            students_to_delete = students_to_delete.filter(batch=batch)

        count, _ = students_to_delete.delete()

        messages.success(request, f'{count} student(s) have been deleted.')

    return redirect('student_list')


@login_required
def delete_student(request, roll_no):
    student = get_object_or_404(Student, roll_no=roll_no)
    student.delete()
    return redirect('student_list')


logger = logging.getLogger(__name__)


@login_required
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
            students = Student.objects.filter(year=year, batch=batch).order_by('roll_no')
            attendance_form = AttendanceForm(request.POST, students=students)
            if attendance_form.is_valid():
                subject = attendance_form.cleaned_data['subject']
                selected_roll_nos = attendance_form.cleaned_data['students']
                in_time = attendance_form.cleaned_data['in_time']
                out_time = attendance_form.cleaned_data['out_time']
                date = attendance_form.cleaned_data['date']
                lab = attendance_form.cleaned_data.get('lab')

                for roll_no in selected_roll_nos:
                    student = Student.objects.get(roll_no=roll_no)
                    Attendance.objects.create(student=student, subject=subject)
                    Session.objects.create(
                        student=student,
                        date=date,
                        subject=subject,
                        in_time=in_time,
                        out_time=out_time,
                        lab=lab
                    )

                    if subject.name == 'C_Language':
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
                    elif subject.name == 'SD':
                        student.sd_attendance += 1
                    elif subject.name == 'DV':
                        student.dv_attendance += 1
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


@login_required
def attendance_summary(request):
    year_batch_form = YearBatchForm()
    session_filter_form = PartFilter(request.POST or None)
    attendance_data = []
    subject_column = None

    if request.method == 'POST':
        if session_filter_form.is_valid():
            year = session_filter_form.cleaned_data['year']
            batch = session_filter_form.cleaned_data['batch']
            subject = session_filter_form.cleaned_data['subject']
            roll_no = session_filter_form.cleaned_data.get('roll_no')

            students = Student.objects.all()
            if year:
                students = students.filter(year=year)
            if batch:
                students = students.filter(batch=batch)
            if roll_no:
                students = students.filter(roll_no=roll_no)

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
                    'SD': student.sd_attendance,
                    'DV': student.dv_attendance,
                }
                if subject:
                    subject_name = subject.name
                    subs = {subject_name: subjects.get(subject_name, 0)}
                    attendance_data.append((student, subs))
                    subject_column = subject_name
                else:
                    attendance_data.append((student, subjects))

            if subject and not attendance_data:
                subject_column = subject.name

    return render(request, 'attendance_summary.html', {
        'year_batch_form': year_batch_form,
        'session_filter_form': session_filter_form,
        'attendance_data': attendance_data,
        'subject_column': subject_column,
    })


@login_required
def reduce_attendance(request):
    if request.method == 'POST':
        form = ReduceAttendanceForm(request.POST)
        if form.is_valid():
            roll_no = form.cleaned_data['roll_no']
            subject = form.cleaned_data['subject']

            try:
                student = Student.objects.get(roll_no=roll_no)
            except Student.DoesNotExist:
                form.add_error('roll_no', 'Student with this roll number does not exist.')
                return render(request, 'reduce_attendance.html', {'form': form})

            student.reduce_attendance(subject)

            success_message = "Attendance reduced successfully."

            return render(request, 'reduce_attendance.html', {
                'form': form,
                'success_message': success_message,
            })

    else:
        form = ReduceAttendanceForm()

    return render(request, 'reduce_attendance.html', {
        'form': form,
    })


@login_required
def session_summary(request):
    form = SessionFilterForm()
    sessions = Session.objects.all()

    if request.method == 'POST':
        form = SessionFilterForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data.get('year')
            batch = form.cleaned_data.get('batch')
            date = form.cleaned_data.get('date')
            subject = form.cleaned_data.get('subject')
            roll_no = form.cleaned_data.get('roll_no')

            if year and year != '':
                sessions = sessions.filter(student__year=year)
            if batch and batch != '':
                sessions = sessions.filter(student__batch=batch)
            if date:
                sessions = sessions.filter(date=date)
            if subject:
                sessions = sessions.filter(subject=subject)
            if roll_no:
                sessions = sessions.filter(student__roll_no=roll_no)

    sessions = sessions.order_by('-date', 'student__roll_no')

    if request.GET.get('export') == 'excel':
        return export_to_excel(sessions)

    return render(request, 'session_summary.html', {
        'form': form,
        'sessions': sessions,
    })


def export_to_excel(sessions):
    data = {
        'ID': [session.id for session in sessions],
        'Roll No': [session.student.roll_no for session in sessions],
        'Name': [session.student.name for session in sessions],
        'Date': [session.date for session in sessions],
        'Subject': [session.subject.name for session in sessions],
        'Lab': [session.lab for session in sessions],
        'In Time': [session.in_time for session in sessions],
        'Out Time': [session.out_time for session in sessions],
    }
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=session_summary.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Session Summary')

    return response


@login_required
def upload_sessions(request):
    if request.method == 'POST':
        form = UploadSessionsForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                student = Student.objects.filter(roll_no=row['Roll No']).first()
                subject = Subject.objects.filter(name=row['Subject']).first()
                if student and subject:
                    Session.objects.update_or_create(
                        id=row['ID'],
                        defaults={
                            'student': student,
                            'date': row['Date'],
                            'subject': subject,
                            'in_time': row['In Time'],
                            'out_time': row['Out Time']
                        }
                    )

            messages.success(request, 'Session records have been updated from the Excel file.')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form = UploadSessionsForm()

    return render(request, 'upload_sessions.html', {'form': form})


@login_required
def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    student = session.student
    subject_name = session.subject.name

    student.reduce_attendance(subject_name)

    session.delete()

    return redirect('session_summary')


@login_required
def attendance_success(request):
    return render(request, 'attendance_success.html')


@login_required
def clear_session_records(request):
    if request.method == 'POST':
        Session.objects.all().delete()
        messages.success(request, 'All session records have been cleared.')
        return redirect('session_summary')

    return render(request, 'confirm_clear.html')


@login_required
def faqs(request):
    return render(request, 'faqs.html')
