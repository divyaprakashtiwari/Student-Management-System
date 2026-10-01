# manager.py
# Keeps track of all the students, and handles the csv file.

import csv
import os

from student import Student, SUBJECTS


class StudentManager:
    FIELDS = ["student_id", "name", "age", "course"] + SUBJECTS

    def __init__(self, filename="students.csv"):
        folder = os.path.dirname(os.path.abspath(__file__))
        self.file = os.path.join(folder, filename)
        self.students = {}      # student_id -> Student object

    # ---- helpers ----
    def next_id(self):
        numbers = []
        for sid in self.students:
            if sid[1:].isdigit():
                numbers.append(int(sid[1:]))
        if len(numbers) == 0:
            return "S2401"
        return "S" + str(max(numbers) + 1)

    def find_student(self, student_id):
        student_id = str(student_id).strip().upper()
        if student_id not in self.students:
            raise Exception("No student found with ID " + student_id)
        return self.students[student_id]

    # ---- features ----
    def add_student(self, name, age, course, marks):
        new_id = self.next_id()
        s = Student(new_id, name, age, course, marks)
        self.students[new_id] = s
        return s

    def get_all(self):
        all_students = list(self.students.values())
        all_students.sort(key=lambda s: s.get_id())
        return all_students

    def search(self, keyword):
        keyword = keyword.strip().lower()
        matches = []
        if keyword == "":
            return matches
        for s in self.get_all():
            if (keyword in s.get_id().lower() or keyword in s.get_name().lower()
                    or keyword in s.get_course().lower()):
                matches.append(s)
        return matches

    def update_details(self, student_id, name=None, age=None, course=None):
        s = self.find_student(student_id)
        if name is not None:
            s.set_name(name)
        if age is not None:
            s.set_age(age)
        if course is not None:
            s.set_course(course)
        return s

    def update_mark(self, student_id, subject, value):
        s = self.find_student(student_id)
        s.set_mark(subject, value)
        return s

    def delete_student(self, student_id):
        s = self.find_student(student_id)
        del self.students[s.get_id()]
        return s

    # ---- average marks ----
    def class_average(self):
        if len(self.students) == 0:
            return None
        total = 0
        for s in self.students.values():
            total = total + s.get_average()
        return total / len(self.students)

    def subject_averages(self):
        result = {}
        if len(self.students) == 0:
            return result
        for sub in SUBJECTS:
            total = 0
            for s in self.students.values():
                total = total + s.get_marks()[sub]
            result[sub] = total / len(self.students)
        return result

    def topper(self):
        best = None
        for s in self.students.values():
            if best is None or s.get_average() > best.get_average():
                best = s
        return best

    # ---- file handling ----
    def load_data(self):
        messages = []
        if not os.path.exists(self.file):
            messages.append("students.csv not found - starting with no records.")
            return messages

        try:
            f = open(self.file, newline="", encoding="utf-8")
        except OSError as e:
            messages.append("Could not read students file: " + str(e))
            return messages

        reader = csv.DictReader(f)
        line_no = 1
        for row in reader:
            line_no += 1
            try:
                marks = {}
                for sub in SUBJECTS:
                    marks[sub] = row[sub]
                s = Student(row["student_id"], row["name"], row["age"], row["course"], marks)
                if s.get_id() in self.students:
                    raise Exception("duplicate ID " + s.get_id())
                self.students[s.get_id()] = s
            except Exception as e:
                messages.append("Skipped line " + str(line_no) + " in students.csv: " + str(e))
        f.close()
        return messages

    def save_data(self):
        try:
            f = open(self.file, "w", newline="", encoding="utf-8")
            writer = csv.writer(f)
            writer.writerow(self.FIELDS)
            for s in self.get_all():
                writer.writerow(s.to_row())
            f.close()
            return True
        except OSError as e:
            print("Error: could not save records (" + str(e) + ")")
            return False
