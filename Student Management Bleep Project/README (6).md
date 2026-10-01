# Student Management System (Mini Project 1)

A console-based Python application that manages student records using
Object-Oriented Programming. Records are stored in a CSV file.

## Features
1. Add students
2. Display students
3. Search students (by ID, name or course)
4. Update student records (name, age, course or any subject's marks)
5. Delete students (with confirmation)
6. Calculate average marks (one student, or a whole-class summary)
7. Save records

## How to run
```
python main.py
```
Requires Python 3.8+ (no external libraries). Keep all files in the same folder.

## Project files
| File | Purpose |
|---|---|
| `person.py` | `Person` (abstract base class) and name/age validation |
| `student.py` | `Student` (derived class), subjects, marks validation, result logic |
| `manager.py` | `StudentManager` (all features + CSV file handling) |
| `main.py` | Console menu |
| `students.csv` | Sample data (16 students) |

## Classes
- **Person (abstract base class)**: Uses the `abc` module. Holds private
  `__name` and `__age` with validated getters/setters, and an abstract
  method `get_details()`.
- **Student (derived class)**: Inherits from `Person`. Adds a read-only
  student ID, a course, and private marks for five subjects. Provides
  `set_mark()`, `average()`, `result()` and CSV helpers.
- **StudentManager**: Keeps all students. Adds, searches, updates and deletes
  students, calculates class/subject averages, finds the topper, and
  loads/saves `students.csv`.
- **Custom exceptions**: `InvalidDataError`, `InvalidMarksError`,
  `StudentNotFoundError`, `DuplicateStudentError`.

## Subjects and results
Each student has marks out of 100 in five subjects: Python Programming,
Data Structures, Database Management, Computer Networks, Business Communication.

| Result | Rule |
|---|---|
| Fail | Any subject below 40 |
| Pass | Average 40 to 49 |
| Second Class | Average 50 to 59 |
| First Class | Average 60 to 74 |
| Distinction | Average 75 and above |

## Sample data
`students.csv` contains 16 fictional students (BCA and B.Sc IT) with a
realistic spread of marks: high achievers, average students, and one student
who fails a subject (S2407, Data Structures 38). New students get the next
free ID (S2417, S2418, ...).

Columns: `student_id, name, age, course, python, data_structures, dbms, networks, communication`

## OOP concepts used
| Concept | Where |
|---|---|
| Classes & Objects | `Person`, `Student`, `StudentManager` |
| Encapsulation | Private attributes with getters/setters in `Person`, `Student`, `StudentManager` |
| Inheritance | `Student(Person)` |
| Abstraction | `Person(ABC)` with `@abstractmethod get_details()` |
| File Handling | Read/write `students.csv` using the `csv` module |
| Exception Handling | Invalid name/age/marks, student not found, missing file, corrupted or duplicate CSV rows |

## Notes
- Invalid input is re-asked instead of crashing the program.
- Bad rows in the CSV are skipped with a message; the rest still load.
- If `students.csv` is missing, the program starts empty and creates it on save.
- Choose option 7 or 8 to save; changes are not saved automatically.
