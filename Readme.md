# Lab Attendance System

This project is a web application designed to manage lab attendance.

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.x
    *   Pip (Python package installer)

2.  **Clone the repository:**
    ```bash
    git clone https://github.com/Hemanth0411/Lab_Attendance
    cd Lab_Attendance
    ```

3.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

4.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```


5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Ensure your virtual environment is activated.
2.  Apply migrations:
    ```bash
    python manage.py migrate
    ```
3.  Create a superuser (optional, for admin access):
    ```bash
    python manage.py createsuperuser
    ```
4.  Run the development server:
    ```bash
    python manage.py runserver
    ```
5.  Open your web browser and navigate to the application URL (usually `http://127.0.0.1:8000/` by default for Django).

## Usage


The application allows you to:
*   Add and edit student details ([`templates/add_students.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/add_students.html), [`templates/edit_student.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/edit_student.html))
*   Import student data ([`templates/import_students.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/import_students.html))
*   Upload session attendance records ([`templates/upload_sessions.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/upload_sessions.html))
*   View attendance summaries ([`templates/attendance_summary.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/attendance_summary.html))
*   Clear data ([`templates/confirm_clear.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/confirm_clear.html))
*   Refer to Frequently Asked Questions ([`templates/faqs.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/faqs.html))

### Login Credentials

As found in `Read_Me.txt`:
Username: Hemanth
Password: Hemanth

## Project Structure

The project includes HTML templates for various pages:
*   [`templates/add_students.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/add_students.html)
*   [`templates/attendance_summary.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/attendance_summary.html)
*   [`templates/confirm_clear.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/confirm_clear.html)
*   [`templates/edit_student.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/edit_student.html)
*   [`templates/faqs.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/faqs.html)
*   [`templates/import_students.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/import_students.html)
*   [`templates/upload_sessions.html`](https://github.com/Hemanth0411/Lab_Attendance/blob/main/templates/upload_sessions.html)
