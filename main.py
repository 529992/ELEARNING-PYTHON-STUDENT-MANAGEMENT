import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect(r'C:\Users\pasin\Desktop\COURSES\PYTHON-B2\DAY 03\ELEARNING-PYTHON-STUDENT-MANAGEMENT\school.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS students (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS courses (
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS enrollment (
             student_id INTEGER,
             course_id INTEGER,
             FOREIGN KEY(student_id) REFERENCES students(id),
             FOREIGN KEY(course_id) REFERENCES courses(id))''')

conn.commit()

# Functions for Students
def add_student():
    name = student_name_entry.get()
    if name:
        c.execute('INSERT INTO students (name) VALUES (?)', (name,))
        conn.commit()
        load_students()
        messagebox.showinfo('Success', 'Student added successfully!')
        student_name_entry.delete(0, tk.END)
    else:
        messagebox.showwarning('Input Error', 'Student name is required!')

def delete_student():
    selected = student_tree.selection()
    if selected:
        student_id = student_tree.item(selected)['values'][0]
        c.execute('DELETE FROM students WHERE id = ?', (student_id,))
        conn.commit()
        load_students()
        messagebox.showinfo('Success', 'Student deleted successfully!')
    else:
        messagebox.showwarning('Selection Error', 'Select a student to delete!')

def load_students():
    for i in student_tree.get_children():
        student_tree.delete(i)
    for row in c.execute('SELECT * FROM students'):
        student_tree.insert('', 'end', values=row)

# Functions for Courses
def add_course():
    name = course_name_entry.get()
    if name:
        c.execute('INSERT INTO courses (name) VALUES (?)', (name,))
        conn.commit()
        load_courses()
        messagebox.showinfo('Success', 'Course added successfully!')
        course_name_entry.delete(0, tk.END)
    else:
        messagebox.showwarning('Input Error', 'Course name is required!')

def delete_course():
    selected = course_tree.selection()
    if selected:
        course_id = course_tree.item(selected)['values'][0]
        c.execute('DELETE FROM courses WHERE id = ?', (course_id,))
        conn.commit()
        load_courses()
        messagebox.showinfo('Success', 'Course deleted successfully!')
    else:
        messagebox.showwarning('Selection Error', 'Select a course to delete!')

def load_courses():
    for i in course_tree.get_children():
        course_tree.delete(i)
    for row in c.execute('SELECT * FROM courses'):
        course_tree.insert('', 'end', values=row)

# Assign student to course
def assign_student():
    student_selected = student_tree.selection()
    course_selected = course_tree.selection()

    if student_selected and course_selected:
        student_id = student_tree.item(student_selected)['values'][0]
        course_id = course_tree.item(course_selected)['values'][0]
        c.execute('INSERT INTO enrollment (student_id, course_id) VALUES (?, ?)', (student_id, course_id))
        conn.commit()
        messagebox.showinfo('Success', 'Student assigned to course!')
    else:
        messagebox.showwarning('Selection Error', 'Select both a student and a course!')

# GUI Setup
root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")
root.configure(bg="#f0f0f0")

style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=25, fieldbackground="#D3D3D3")
style.map('Treeview', background=[('selected', '#4a6984')])

# Create tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

students_frame = ttk.Frame(notebook)
courses_frame = ttk.Frame(notebook)
assign_frame = ttk.Frame(notebook)

notebook.add(students_frame, text="Manage Students")
notebook.add(courses_frame, text="Manage Courses")
notebook.add(assign_frame, text="Assign Students")

# Students Tab
student_name_entry = ttk.Entry(students_frame, width=30)
student_name_entry.grid(row=0, column=0, padx=10, pady=10)

add_student_btn = ttk.Button(students_frame, text="Add Student", command=add_student)
add_student_btn.grid(row=0, column=1, padx=10, pady=10)

delete_student_btn = ttk.Button(students_frame, text="Delete Student", command=delete_student)
delete_student_btn.grid(row=0, column=2, padx=10, pady=10)

student_tree = ttk.Treeview(students_frame, columns=('ID', 'Name'), show='headings')
student_tree.heading('ID', text='ID')
student_tree.heading('Name', text='Name')
student_tree.column('ID', width=50)
student_tree.column('Name', width=200)
student_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

students_frame.grid_columnconfigure(0, weight=1)
students_frame.grid_rowconfigure(1, weight=1)

# Courses Tab
course_name_entry = ttk.Entry(courses_frame, width=30)
course_name_entry.grid(row=0, column=0, padx=10, pady=10)

add_course_btn = ttk.Button(courses_frame, text="Add Course", command=add_course)
add_course_btn.grid(row=0, column=1, padx=10, pady=10)

delete_course_btn = ttk.Button(courses_frame, text="Delete Course", command=delete_course)
delete_course_btn.grid(row=0, column=2, padx=10, pady=10)

course_tree = ttk.Treeview(courses_frame, columns=('ID', 'Name'), show='headings')
course_tree.heading('ID', text='ID')
course_tree.heading('Name', text='Name')
course_tree.column('ID', width=50)
course_tree.column('Name', width=200)
course_tree.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

courses_frame.grid_columnconfigure(0, weight=1)
courses_frame.grid_rowconfigure(1, weight=1)

# Assign Tab
assign_label = ttk.Label(assign_frame, text="Select a student and a course, then click 'Assign'")
assign_label.pack(pady=10)

assign_btn = ttk.Button(assign_frame, text="Assign Student to Course", command=assign_student)
assign_btn.pack(pady=10)

# Load initial data
load_students()
load_courses()

root.mainloop()