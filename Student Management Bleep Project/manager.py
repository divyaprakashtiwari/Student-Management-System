"""manager.py - StudentManager class.

Handles adding, displaying, searching, updating and deleting students,
calculating average marks, and saving/loading records from a CSV file.
"""

import csv
import os

from student import Student, SUBJECT_KEYS


class StudentNotFoundError(Exception):
    """Raised when a student ID does not exist."""


class DuplicateStudentError(Exception):
    """Raised when two students share the same ID."""


class StudentManager:
    FIELDS = ["student_id", "name", "age", "course"] + SUBJECT_KEYS

    def __init__(self, filename="students.csv"):
        base = os.path.dirname(os.path.abspath(__file__))
        self.__file = os.path.join(base, filename)
        self.__students = {}          # student_id -> Student

    # ---------- helpers ----------
    def __next_id(self):
        numbers = [int(sid[1:]) for sid in self.__students if sid[1:].isdigit()]
        return f"S{max(numbers) + 1}" if numbers else "S2401"

    def get_student(self, student_id):
        student_id = str(student_id).strip().upper()
        if student_id not in self.__students:
            raise StudentNotFoundError(f"No student found with ID {student_id}.")
        return self.__students[student_id]

    # ---------- features ----------
    def add_student(self, name, age, course, marks):
        student = Student(self.__next_id(), name, age, course, marks)
        self.__students[student.student_id] = student
        return student

    def all_students(self):
        return sorted(self.__students.values(), key=lambda s: s.student_id)

    def search(self, keyword):
        """Case-insensitive search on ID, name or course."""
        keyword = str(keyword).strip().lower()
        if not keyword:
            return []
        return [s for s in self.all_students()
                if keyword in s.student_id.lower()
                or keyword in s.name.lower()
                or keyword in s.course.lower()]

    def update_details(self, student_id, name=None, age=None, course=None):
        student = self.get_student(student_id)
        if name is not None:
            student.name = name
        if age is not None:
            student.age = age
        if course is not None:
            student.course = course
        return student

    def update_mark(self, student_id, subject, value):
        student = self.get_student(student_id)
        student.set_mark(subject, value)
        return student

    def delete_student(self, student_id):
        student = self.get_student(student_id)
        del self.__students[student.student_id]
        return student

    # ---------- average marks ----------
    def class_average(self):
        """Average of every student's average, or None if there are no students."""
        if not self.__students:
            return None
        return sum(s.average() for s in self.__students.values()) / len(self.__students)

    def subject_averages(self):
        """Dictionary of subject key -> class average in that subject."""
        if not self.__students:
            return {}
        count = len(self.__students)
        return {k: sum(s.marks[k] for s in self.__students.values()) / count
                for k in SUBJECT_KEYS}

    def topper(self):
        if not self.__students:
            return None
        return max(self.__students.values(), key=lambda s: s.average())

    # ---------- file handling ----------
    def load_data(self):
        """Load students from CSV. Returns a list of messages about any problems."""
        messages = []
        try:
            with open(self.__file, newline="", encoding="utf-8") as f:
                for line_no, row in enumerate(csv.DictReader(f), start=2):
                    try:
                        student = Student.from_row(row)
                        if student.student_id in self.__students:
                            raise DuplicateStudentError(
                                f"duplicate ID {student.student_id}")
                        self.__students[student.student_id] = student
                    except (ValueError, DuplicateStudentError) as e:
                        messages.append(f"Skipped line {line_no} in students.csv: {e}")
        except FileNotFoundError:
            messages.append("students.csv not found - starting with no records.")
        except OSError as e:
            messages.append(f"Could not read students file: {e}")
        return messages

    def save_data(self):
        """Write all students to CSV. Returns True if successful."""
        try:
            with open(self.__file, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(self.FIELDS)
                for student in self.all_students():
                    writer.writerow(student.to_row())
            return True
        except OSError as e:
            print(f"Error: could not save records ({e}).")
            return False
