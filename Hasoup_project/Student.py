import sqlite3
class Student :
    def __init__(self, student_id, first_name, last_name, age, grade, registration_date):
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._age = age
        self._grade = grade
        self._registration_date = registration_date

    # --- getters ---
    @property
    def student_id(self):
        return self._student_id
    
    @property
    def first_name(self):
        return self._first_name
    
    @property
    def last_name(self):
        return self._last_name

    @property
    def age(self):
        return self._age

    @property
    def grade(self):
        return self._grade

    @property
    def registration_date(self):
        return self._registration_date
    
    # --- setters ---
    @student_id.setter
    def student_id(self, value):
        if isinstance(value, int):
            self._student_id = value
        else :
            raise ValueError("the student id must be str only")

    @first_name.setter
    def first_name(self, value):
        if isinstance(value, str):
            self._first_name = value
        else :
            raise ValueError("the first name must be str only")

    @last_name.setter
    def last_name(self, value):
        if isinstance(value, str):
            self._last_name = value
        else :
            raise ValueError("the last name must be str only")

    @age.setter
    def age(self, value):
        if isinstance(value, int) and value > 6:
            self._age = value
        else:
            raise ValueError("Age must be an integer bigger than 6.")

    @grade.setter
    def grade(self, value):
        if isinstance(value, int):
            self._grade = value
        else :
            raise ValueError("the grade must be int only")

    @registration_date.setter
    def registration_date(self, value):
        if isinstance(value, str):
            self._registration_date = value
        else :
            raise ValueError("registration date must be a str only.")
    
    # --- Hash and Equal ---
    def __hash__(self):
        return hash(self._student_id)
    
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._student_id == other._student_id
    
    def __repr__(self):
        return f"Student(student_id = {self.student_id}, name = {self.first_name} {self.last_name}, age = {self.age}, grade = {self.grade}, registration date = {self.registration_date} )"

    def add_student(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "INSERT INTO students (student_id, first_name, last_name, age, grade, registration_date) VALUES (?, ?, ?, ?, ?, ?)"
                cursor.execute(query, (self.student_id, self.first_name, self.last_name, self.age, self.grade, self.registration_date,))
                conn.commit()
                print("The student has been added successfully.")
        except sqlite3.Error as e :
             print(f"Database error: {e}")
             conn.rollback()           

    def update_student(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "UPDATE students SET first_name = ?, last_name = ? , age = ?, grade = ? , registration_date = ?  WHERE student_id = ?;"
                cursor.execute(query, (self.first_name, self.last_name, self.age, self.grade, self.registration_date, self.student_id,))
                conn.commit()
                print("Changes have been applied successfully.")
        except sqlite3.Error as e :
            print(f"Database error: {e}")
            conn.rollback()
    
    def remove_student(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
              conn.execute("PRAGMA foreign_keys = ON")
              cursor = conn.cursor()
              query = "DELETE FROM students WHERE student_id = ?;"
              cursor.execute(query,(self.student_id,))
              conn.commit()
              print("Student removed successfully.")
        except sqlite3.Error as e:
          print(f"Database error: {e}")
          conn.rollback()
    
    @classmethod
    def from_row(cls, row):
        if row and len(row) == 6:
            try:
                student_id, first_name, last_name, age, grade, registration_date = row
                if not isinstance(student_id, int) or not isinstance(age, int) or not isinstance(grade, int):
                    print("Warning: Invalid data types in row. Skipping.")
                    return None
                
                return cls(student_id, first_name, last_name, age, grade, registration_date)
            except ValueError as e:
                print(f"Error creating student from row: {e}")
                return None

        else:
            print("Invalid row format.  Expected 6 elements.")
            return None 
    
    @classmethod
    def get_student_by_id(cls, student_id):
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "SELECT student_id, first_name, last_name, age, grade, registration_date FROM students WHERE student_id = ?"
                cursor.execute(query, (student_id,))
                row = cursor.fetchone() 

                if row:
                    return cls.from_row(row) 
                else:
                    #print(f"Student with ID {student_id} not found.")
                    return False

        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None  