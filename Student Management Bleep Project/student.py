# student.py
# Person (abstract base class) and Student (inherits from Person).
# Kept in one file since Person only exists to support Student here.

from abc import ABC, abstractmethod

MIN_AGE = 15
MAX_AGE = 60

# subjects every student has marks for
SUBJECTS = ["python", "data_structures", "dbms", "networks", "communication"]

SUBJECT_NAMES = {
    "python": "Python Programming",
    "data_structures": "Data Structures",
    "dbms": "Database Management",
    "networks": "Computer Networks",
    "communication": "Business Communication",
}

PASS_MARK = 40


def validate_name(name):
    name = name.strip()
    if name == "":
        raise ValueError("Name cannot be empty")
    for ch in name:
        if not (ch.isalpha() or ch in " .'-"):
            raise ValueError("Name should only contain letters and spaces")
    return name


def validate_age(age):
    try:
        age = int(age)
    except ValueError:
        raise ValueError("Age must be a whole number")
    if age < MIN_AGE or age > MAX_AGE:
        raise ValueError("Age must be between " + str(MIN_AGE) + " and " + str(MAX_AGE))
    return age


def validate_course(course):
    course = course.strip()
    if course == "":
        raise ValueError("Course cannot be empty")
    return course


def validate_mark(value):
    try:
        value = int(value)
    except ValueError:
        raise ValueError("Marks must be a whole number between 0 and 100")
    if value < 0 or value > 100:
        raise ValueError("Marks must be between 0 and 100")
    return value


class Person(ABC):
    # Base class for anyone with a name and an age.
    # Abstract because this project only ever uses it through Student,
    # but it still shows the abstraction + inheritance requirement.

    def __init__(self, name, age):
        self.__name = ""
        self.__age = 0
        self.set_name(name)
        self.set_age(age)

    # ---- getters and setters (encapsulation) ----
    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = validate_name(name)

    def get_age(self):
        return self.__age

    def set_age(self, age):
        self.__age = validate_age(age)

    # every subclass has to say how it shows its own details
    @abstractmethod
    def get_details(self):
        pass


class Student(Person):
    def __init__(self, student_id, name, age, course, marks):
        super().__init__(name, age)

        student_id = str(student_id).strip().upper()
        if student_id == "":
            raise ValueError("Student ID cannot be empty")
        self.__student_id = student_id        # id never changes once set

        self.__course = ""
        self.set_course(course)

        self.__marks = {}
        for sub in SUBJECTS:
            if sub not in marks:
                raise ValueError("Missing marks for " + sub)
            self.set_mark(sub, marks[sub])

    # ---- getters and setters ----
    def get_id(self):
        return self.__student_id

    def get_course(self):
        return self.__course

    def set_course(self, course):
        self.__course = validate_course(course)

    def get_marks(self):
        # return a copy so no one can mess with the real dict from outside
        return dict(self.__marks)

    def set_mark(self, subject, value):
        if subject not in SUBJECTS:
            raise ValueError("Unknown subject: " + subject)
        self.__marks[subject] = validate_mark(value)

    # ---- calculations ----
    def get_average(self):
        total = 0
        for m in self.__marks.values():
            total = total + m
        return total / len(self.__marks)

    def get_result(self):
        # fail if even one subject is below the pass mark
        for m in self.__marks.values():
            if m < PASS_MARK:
                return "Fail"

        avg = self.get_average()
        if avg >= 75:
            return "Distinction"
        elif avg >= 60:
            return "First Class"
        elif avg >= 50:
            return "Second Class"
        else:
            return "Pass"

    # ---- required because Person is abstract ----
    def get_details(self):
        return (self.__student_id + " | " + self.get_name() + " | Age " +
                str(self.get_age()) + " | " + self.__course + " | Avg " +
                format(self.get_average(), ".2f") + " | " + self.get_result())

    def __str__(self):
        return self.get_details()

    # ---- turn into a list for saving to csv ----
    def to_row(self):
        row = [self.__student_id, self.get_name(), self.get_age(), self.__course]
        for sub in SUBJECTS:
            row.append(self.__marks[sub])
        return row
