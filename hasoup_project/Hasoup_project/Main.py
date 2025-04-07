from Student import Student
from Lesson import Lesson
import sqlite3
def object_exist(object_type, id):
    if object_type == "S" :
       return Student.get_student_by_id(id)
    else :
        return Lesson.get_lesson_by_id(id)

def no_id_redundancy(message, error_message, object_type):
    while True :
        user_input = is_it_int(message, error_message)
        if object_exist(object_type, user_input) == False :
            return user_input
        else :
            print("this id already in the system")

def no_name_redundancy(message):
    while True :
        name = input(f"{message}\n")
        if Lesson.get_lesson_by_name(name) == False :
            return name
        else :
            print("this name already in the system")

def bool_only(message, error_message):
    while True :
        user_input = input(f"{message}\n").upper()
        if user_input == "Y" or user_input == "N" :
            return user_input
        else :
            print(error_message)

def is_it_int(message, error_message):
    while True :
        user_input = input(f"{message}\n")
        try :
            return int(user_input)
        except ValueError :
            print(error_message)

def add_students_to_lesson(lesson_id, lesson_name):    
    num_to_add = is_it_int("How many students do you want to add to this lesson?", "please enter only digits")
    for i in range(num_to_add):
        while True:
            student_id = is_it_int(f"Enter the ID of student #{i+1} to add:", "please enter only digits for student id")
            student = Student.get_student_by_id(student_id)
            if not student:
                print("This student ID does not exist in the system.")
                continue
                
            try:
                with sqlite3.connect('School_DB.db') as conn:
                    cursor = conn.cursor()
                    query = "SELECT * FROM student_lesson_enrollments WHERE lesson_id = ? AND student_id = ?"
                    cursor.execute(query, (lesson_id, student_id))
                    if cursor.fetchone():
                        print("This student is already enrolled in this lesson.")
                        continue
                    
                    query = "INSERT INTO student_lesson_enrollments (lesson_id, student_id) VALUES (?, ?)"
                    cursor.execute(query, (lesson_id, student_id))
                    conn.commit()
                    print(f"Student {student_id} successfully enrolled in '{lesson_name}'")
                    break
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                continue
    
def remove_students_from_lesson(lesson_id, lesson_name):
    enrolled_students = []
    try:
        with sqlite3.connect('School_DB.db') as conn:
            cursor = conn.cursor()
            query = """
            SELECT s.student_id, s.first_name, s.last_name 
            FROM students s 
            JOIN student_lesson_enrollments sle ON s.student_id = sle.student_id 
            WHERE sle.lesson_id = ?
            """
            cursor.execute(query, (lesson_id,))
            enrolled_students = cursor.fetchall()
            
            if not enrolled_students:
                print("No students currently enrolled in this lesson.")
                return
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return
    
    num_to_remove = is_it_int("How many students do you want to remove from this lesson?", "please enter only digits")
    if num_to_remove > len(enrolled_students):
        print(f"There are only {len(enrolled_students)} students enrolled in this lesson.")
    
    for i in range(len(enrolled_students)):
        while True:
            student_id = is_it_int(f"Enter the ID of student #{i+1} to remove:", "please enter only digits for student id")
            try:
                with sqlite3.connect('School_DB.db') as conn:
                    cursor = conn.cursor()
                    query = "SELECT * FROM student_lesson_enrollments WHERE lesson_id = ? AND student_id = ?"
                    cursor.execute(query, (lesson_id, student_id))
                    if not cursor.fetchone():
                        print("This student is not enrolled in this lesson.")
                        continue

                    query = "DELETE FROM student_lesson_enrollments WHERE lesson_id = ? AND student_id = ?"
                    cursor.execute(query, (lesson_id, student_id))
                    conn.commit()
                    print(f"Student {student_id} successfully removed from '{lesson_name}'")
                    break
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                continue

def add_students():
    num_of_students = is_it_int("How many student do you want to add", "please enter only digits")
    for i in range(num_of_students):
        student_id = no_id_redundancy(f"Enter the id for student#{i+1}.", "please enter only digits for student id","S")
        f_name = input(f"Enter the first name for student#{i+1}.\n")
        l_name = input(f"Enter the last name for student#{i+1}.\n")
        age = is_it_int(f"Enter the age for student#{i+1}.", "please enter only digits for age")
        grade = is_it_int(f"Enter the grade for student#{i+1}.", "please enter only digits for grade")
        reg_date = input(f"Enter the registration date for student#{i+1}.\n")
        students_to_add[student_id] = Student(student_id, f_name, l_name, age, grade, reg_date)
        
        there_is_a_lessons = bool_only(f"Does student {student_id} have any lessons?", "please enter y or n only")
        if there_is_a_lessons == "N":
            continue
        else:            
            lessons_number = is_it_int("How many lessons does the student have?", "please enter digits only")
            for j in range(lessons_number):
                show_lessons()
                lesson_id = is_it_int(f"Enter the id for lesson# {j+1}", "please enter only digits for lesson id")
                existing_lesson = Lesson.get_lesson_by_id(lesson_id)

                if existing_lesson:
                    print(f"we will add student {student_id} to the existing Lesson '{existing_lesson.lesson_name}' with ID {existing_lesson.lesson_id}")
                    lesson_id = existing_lesson.lesson_id
                else:
                    print(f"Creating new lesson: '{existing_lesson.lesson_name}'")
                    lesson_id = no_id_redundancy(f"Enter the id for '{existing_lesson.lesson_name}'", "please enter only digits for lesson id", "L")
                    lessons_to_add[lesson_id] = Lesson(lesson_id, existing_lesson.lesson_name)
                st_les.append((lesson_id, student_id))

def remove_students():
    num_of_students = is_it_int("How many student do you want to remove", "please enter only digits")
    for i in range(num_of_students):
        while True :
            student_id = is_it_int(f"Enter the id for student#{i+1}.", "please enter only digits for student id")
            if Student.get_student_by_id(student_id) != False :
                students_to_remove.append(Student.get_student_by_id(student_id))
                break
            else :
                print("this id is not in the system")

def show_students():
    num_of_students = is_it_int("How many student do you want to show", "please enter only digits")
    for i in range(num_of_students):
        while True :
            student_id = is_it_int(f"Enter the id for student#{i+1}.", "please enter only digits for student id")
            if Student.get_student_by_id(student_id) != False :
                students_to_show.append(Student.get_student_by_id(student_id))
                break
            else :
                print("this id is not in the system")

def update_students():
    num_of_students = is_it_int("How many student do you want to update", "please enter only digits")
    for i in range(num_of_students):
        while True :
            student_id = is_it_int(f"Enter the id for student#{i+1}.", "please enter only digits for student id")
            if Student.get_student_by_id(student_id) != False :
                break
            else :
                print("this id is not in the system")

        student = Student.get_student_by_id(student_id)
        f_name = input(f"Enter the new first name for student#{i+1}. enter i if you want to keep this without change\n").upper()
        if f_name != "I" :
            student.first_name = f_name
        l_name = input(f"Enter the new last name for student#{i+1}. enter i if you want to keep this without change\n").upper()
        if l_name != "I" :
            student.last_name = l_name
        age = is_it_int(f"Enter the new age for student#{i+1}. enter -1 if you want to keep this without change", "please enter only digits for the age")
        if age != -1 :
            student.age = age
        grade = is_it_int(f"Enter the new grade for student#{i+1}. enter -1 if you want to keep this without change", "please enter only digits for the grade")
        if grade != -1 :
            student.grade = grade
        reg_date = input(f"Enter the new registration date for student#{i+1}. enter i if you want to keep this without change\n").upper()
        if reg_date != "I" :
            student.registration_date = reg_date
        students_to_update.append(student)

def add_lessons():
    num_of_lessons = is_it_int("How many lessons do you want to add", "please enter only digits")
    for i in range(num_of_lessons):
        lesson_name = no_name_redundancy(f"Enter the name for lesson# {i+1}")
        lesson_id = no_id_redundancy(f"Enter the id of {lesson_name}", "please enter only digits for lesson id","L")
        lessons_to_add[lesson_id] = Lesson(lesson_id, lesson_name)

def remove_lessons():
    num_of_lessons = is_it_int("How many lessons do you want to remove", "please enter only digits")
    for i in range(num_of_lessons):
        while True:
            lesson_id = is_it_int(f"Enter the id for lesson#{i+1}.", "please enter only digits for lesson id")
            if Lesson.get_lesson_by_id(lesson_id) != False:
                lessons_to_remove.append(Lesson.get_lesson_by_id(lesson_id))
                break
            else:
                print("this id is not in the system")

def update_lessons():
    num_of_lessons = is_it_int("How many lessons do you want to update", "please enter only digits")
    for i in range(num_of_lessons):
        show_lessons()
        while True:
            lesson_id = is_it_int(f"Enter the id for lesson#{i+1}.", "please enter only digits for lesson id")
            lesson = Lesson.get_lesson_by_id(lesson_id)
            if lesson != False:
                break
            else:
                print("this id is not in the system")

        lesson_name = input(f"Enter the new name for lesson#{i+1}. Enter i if you want to keep this without change\n").upper()
        if lesson_name != "I":
            lesson.lesson_name = lesson_name
        
        modify_enrollments = bool_only(f"Do you want to modify student enrollments for this lesson (ID: {lesson_id})?", "please enter y or n only")
        
        if modify_enrollments == "Y":
            print("Do you want to:")
            print("1. Add students to this lesson")
            print("2. Remove students from this lesson")
            print("3. Skip enrollment modifications")
            choice = is_it_int("Enter your choice (1-3):", "Please enter a number between 1 and 3")
            
            if choice == 1 :
                add_students_to_lesson(lesson_id, lesson.lesson_name)
            
            if choice == 2 :
                remove_students_from_lesson(lesson_id, lesson.lesson_name)
        
        lessons_to_update.append(lesson)

def show_lessons():
    try:
        with sqlite3.connect('School_DB.db') as conn:
            cursor = conn.cursor()
            query = "SELECT lesson_id, lesson_name FROM lessons"
            cursor.execute(query)
            lessons = cursor.fetchall()
            
            if not lessons:
                print("No lessons found in the system.")
            else:
                print("\n--- Available Lessons ---")
                for lesson in lessons:
                    lesson_id, lesson_name = lesson
                    print(f"ID: {lesson_id}, Name: {lesson_name}")
                print("------------------------\n")
                
    except sqlite3.Error as e:
        print(f"Database error: {e}")

while True :

    print("----What Do You Want To Do----") 
    print("""Add student (A)
Delete student (D)
Update student info (U)
Show student info (S)
Add lesson (AL)
Delete lesson (DL)
Update lesson (UL)
Show lessons (SL)
Quit (Q)""")

    st_les = list()
    lessons_to_add = dict()
    students_to_add = dict()
    students_to_show = list()
    lessons_to_update = list()
    lessons_to_remove = list()
    students_to_remove = list()
    students_to_update = list()

    user_choice = input("Enter the appropriate letter for your choice.\n").upper()
    if user_choice == "A" :
        add_students()
        for i in students_to_add.values() :
            i.add_student()
        for i in lessons_to_add.values() :
            i.add_lesson()
        for lesson_id, student_id in st_les:
            try:
                with sqlite3.connect('School_DB.db') as conn:
                    cursor = conn.cursor()
                    query = "INSERT INTO student_lesson_enrollments (lesson_id, student_id) VALUES (?,?);"
                    cursor.execute(query, (lesson_id, student_id))
                    conn.commit()
                    print("Done.")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
                conn.rollback()
    elif user_choice == "D" :
        remove_students()
        for i in students_to_remove :
            i.remove_student()
    elif user_choice == "U" :
        update_students()
        for i in students_to_update :
            i.update_student()
    elif user_choice == "S" :
        show_students()
        for i in students_to_show :
            try:
                with sqlite3.connect('School_DB.db') as conn:
                    cursor = conn.cursor()
                    query = "SELECT l.lesson_name FROM students s JOIN student_lesson_enrollments sle ON s.student_id = sle.student_id JOIN lessons l ON sle.lesson_id = l.lesson_id WHERE s.student_id = ?; "
                    cursor.execute(query, (i.student_id,))
                    lessons = cursor.fetchall()
                    print(f"{i} has the lessons {lessons}")
            except sqlite3.Error as e:
                print(f"Database error: {e}")
    elif user_choice == "AL" :
        add_lessons()
        for i in lessons_to_add.values():
            i.add_lesson()
    elif user_choice == "DL" :
        remove_lessons()
        for i in lessons_to_remove:
            i.remove_lesson()
    elif user_choice == "UL" :
        update_lessons()
        for i in lessons_to_update:
            i.update_Lesson()
    elif user_choice == "SL" :
        show_lessons()
    elif user_choice == "Q" :
        break
    else :
        print("please enter only one of [A, D, U, S, AL, DL, US, SL, Q]")

        