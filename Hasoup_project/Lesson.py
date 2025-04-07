import sqlite3
class Lesson :
    def __init__(self, lesson_id, lesson_name):
        self._lesson_id = lesson_id
        self._lesson_name = lesson_name
    
    # --- getters ---
    @property
    def lesson_id(self):
        return self._lesson_id

    @property
    def lesson_name(self):
        return self._lesson_name
    
    # --- setters ---
    @lesson_id.setter
    def lesson_id(self, value):
        if isinstance(value, int):
            self._lesson_id = value
        else :
            raise ValueError("the lesson id must be Int only")
        
    @lesson_name.setter
    def lesson_name(self, value):
        if isinstance(value, str):
            self._lesson_name = value
        else :
            raise ValueError("the lesson name must be str only")

    #Hash and Equal
    def __hash__(self):
        return hash(self._lesson_id)
    
    def __eq__(self, other):
        if not isinstance(other, Lesson):
            return NotImplemented
        return self._lesson_id == other._lesson_id
    
    def __str__(self):
        return f"Lesson(lesson name: {self.lesson_name} has id: {self.lesson_id})"

    def add_lesson(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "INSERT INTO lessons (lesson_id, lesson_name) VALUES (?, ?)"
                cursor.execute(query, (self.lesson_id, self.lesson_name))
                conn.commit()
                print("The lesson has been added successfully.")
        except sqlite3.Error as e :
             print(f"Database error: {e}")
             conn.rollback()
            
    def remove_lesson(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
              conn.execute("PRAGMA foreign_keys = ON")
              cursor = conn.cursor()
              query = "DELETE FROM lessons WHERE lesson_id = ?;"
              cursor.execute(query,(self.lesson_id,))
              conn.commit()
              print("Lesson removed successfully.")
        except sqlite3.Error as e:
          print(f"Database error: {e}")
          conn.rollback()
    
    def update_Lesson(self):
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                # Update only the lesson_name, using lesson_id in the WHERE clause
                query = "UPDATE lessons SET lesson_name = ? WHERE lesson_id = ?;"
                cursor.execute(query, (self.lesson_name, self.lesson_id))  # Corrected parameters
                if cursor.rowcount == 0:
                    print("No lesson found with that ID.")
                else:
                    conn.commit()
                    print("Changes have been applied successfully.")
        except sqlite3.Error as e :
            print(f"Database error: {e}")
            conn.rollback()

    @classmethod
    def from_row(cls, row) :
        if row and len(row) == 2:
            lesson_id, lesson_name = row
            return cls(lesson_id, lesson_name)
        else:
            print("Invalid row format. Expected 2 elements.")
            return None

    @classmethod
    def get_lesson_by_id(cls, lesson_id) :
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "SELECT lesson_id, lesson_name FROM lessons WHERE lesson_id = ?"
                cursor.execute(query, (lesson_id,))
                row = cursor.fetchone()

                if row:
                    return cls.from_row(row)
                else:
                    #print(f"Lesson with ID {lesson_id} not found.")
                    return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    @classmethod
    def get_lesson_by_name(cls, lesson_name) :
        try:
            with sqlite3.connect('School_DB.db') as conn:
                cursor = conn.cursor()
                query = "SELECT lesson_id, lesson_name FROM lessons WHERE lesson_name = ?"
                cursor.execute(query, (lesson_name,))
                row = cursor.fetchone()

                if row:
                    return cls.from_row(row)
                else:
                    #print(f"Lesson with name {lesson_name} not found.")
                    return False
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None