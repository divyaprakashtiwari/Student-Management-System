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
| `student.py` | `Person` (abstract base class) and `Student` (derived class): getters/setters, validation, result logic |
| `manager.py` | `StudentManager` (all features + CSV file handling) |
| `main.py` | Console menu |
| `students.csv` | Sample data (16 students) |

## Classes
- **Person (abstract base class)**: Uses the `abc` module. Holds a private
  name and age, accessed through `get_name()`/`set_name()` and
  `get_age()`/`set_age()`, and an abstract method `get_details()`.
- **Student (derived class)**: Inherits from `Person`. Adds a read-only
  student ID, a course, and private marks for five subjects. Provides
  `set_mark()`, `get_average()`, `get_result()` and a `to_row()` helper
  for saving to CSV.
- **StudentManager**: Keeps all students in a dictionary. Adds, searches,
  updates and deletes students, calculates class/subject averages, finds
  the topper, and loads/saves `students.csv`.
- **Validation functions**: `validate_name`, `validate_age`,
  `validate_course`, `validate_mark` (in `student.py`) raise `ValueError`
  with a clear message when given bad input, so the menu can ask again.

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
| Encapsulation | Private attributes with `get_x()`/`set_x()` methods in `Person`, `Student`, `StudentManager` |
| Inheritance | `Student(Person)` |
| Abstraction | `Person(ABC)` with `@abstractmethod get_details()` |
| File Handling | Read/write `students.csv` using the `csv` module |
| Exception Handling | Invalid name/age/marks (`ValueError`), student not found, missing file, corrupted or duplicate CSV rows |

## Notes
- Invalid input is re-asked instead of crashing the program.
- Bad rows in the CSV are skipped with a message; the rest still load.
- If `students.csv` is missing, the program starts empty and creates it on save.
- Choose option 7 or 8 to save; changes are not saved automatically.
