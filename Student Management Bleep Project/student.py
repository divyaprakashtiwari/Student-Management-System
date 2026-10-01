"""student.py - Student class (derived from Person).

Covers: Inheritance (Student extends Person), Encapsulation (private ID,
course and marks), Exception handling (InvalidMarksError).
"""

from person import Person, InvalidDataError

# (csv column, full subject name, short label used in tables)
SUBJECTS = [
    ("python", "Python Programming", "Python"),
    ("data_structures", "Data Structures", "DS"),
    ("dbms", "Database Management", "DBMS"),
    ("networks", "Computer Networks", "CN"),
    ("communication", "Business Communication", "Comm"),
]
SUBJECT_KEYS = [s[0] for s in SUBJECTS]
PASS_MARK = 40


class InvalidMarksError(ValueError):
    """Raised when marks are not a whole number between 0 and 100."""


def validate_mark(value):
    """Return marks as an int (0-100) or raise InvalidMarksError."""
    try:
        mark = int(str(value).strip())
    except ValueError:
        raise InvalidMarksError("Marks must be a whole number between 0 and 100.")
    if not 0 <= mark <= 100:
        raise InvalidMarksError("Marks must be between 0 and 100.")
    return mark


def validate_course(value):
    """Return a cleaned course name or raise InvalidDataError."""
    value = " ".join(str(value).split())
    if not value:
        raise InvalidDataError("Course cannot be empty.")
    return value


class Student(Person):
    """A student with an ID, a course and marks in each subject."""

    def __init__(self, student_id, name, age, course, marks):
        super().__init__(name, age)
        student_id = str(student_id).strip().upper()
        if not student_id:
            raise InvalidDataError("Student ID cannot be empty.")
        self.__student_id = student_id
        self.__course = validate_course(course)
        self.__marks = {}
        for key in SUBJECT_KEYS:
            if key not in marks:
                raise InvalidMarksError(f"Missing marks for '{key}'.")
            self.set_mark(key, marks[key])

    # ---------- getters / setters ----------
    @property
    def student_id(self):
        return self.__student_id          # read-only: an ID never changes

    @property
    def course(self):
        return self.__course

    @course.setter
    def course(self, value):
        self.__course = validate_course(value)

    @property
    def marks(self):
        return dict(self.__marks)         # copy, so callers cannot edit directly

    def set_mark(self, subject, value):
        if subject not in SUBJECT_KEYS:
            raise InvalidMarksError(f"Unknown subject: {subject}")
        self.__marks[subject] = validate_mark(value)

    # ---------- calculations ----------
    def average(self):
        return sum(self.__marks.values()) / len(self.__marks)

    def result(self):
        """Fail if any subject is below the pass mark, otherwise grade by average."""
        if any(m < PASS_MARK for m in self.__marks.values()):
            return "Fail"
        avg = self.average()
        if avg >= 75:
            return "Distinction"
        if avg >= 60:
            return "First Class"
        if avg >= 50:
            return "Second Class"
        return "Pass"

    # ---------- required by Person ----------
    def get_details(self):
        return (f"{self.student_id} | {self.name} | Age {self.age} | {self.course} | "
                f"Avg {self.average():.2f} | {self.result()}")

    # ---------- CSV helpers ----------
    def to_row(self):
        return [self.student_id, self.name, self.age, self.course] + \
               [self.__marks[k] for k in SUBJECT_KEYS]

    @classmethod
    def from_row(cls, row):
        marks = {k: (row.get(k) or "") for k in SUBJECT_KEYS}
        return cls(row.get("student_id") or "", row.get("name") or "",
                   row.get("age") or "", row.get("course") or "", marks)
