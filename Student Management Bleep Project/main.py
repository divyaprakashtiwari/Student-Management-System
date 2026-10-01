"""main.py - Console menu for the Student Management System."""

from manager import StudentManager, StudentNotFoundError
from person import validate_name, validate_age
from student import SUBJECTS, validate_mark, validate_course

MENU = """
========== STUDENT MANAGEMENT SYSTEM ==========
1. Add student
2. Display all students
3. Search students
4. Update student record
5. Delete student
6. Calculate average marks
7. Save records
8. Save and exit
===============================================
"""


def ask(prompt, validator):
    """Keep asking until the validator accepts the input."""
    while True:
        try:
            return validator(input(prompt))
        except ValueError as e:          # InvalidDataError / InvalidMarksError
            print(f"  Invalid input: {e}")


def print_table(students):
    header = f"{'ID':<7}{'Name':<23}{'Age':<5}{'Course':<9}"
    header += "".join(f"{short:>7}" for _, _, short in SUBJECTS)
    header += f"{'Avg':>8}  Result"
    print(header)
    print("-" * (len(header) + 6))
    for s in students:
        marks = s.marks
        row = f"{s.student_id:<7}{s.name[:22]:<23}{s.age:<5}{s.course:<9}"
        row += "".join(f"{marks[key]:>7}" for key, _, _ in SUBJECTS)
        row += f"{s.average():>8.2f}  {s.result()}"
        print(row)


def add_student(manager):
    name = ask("Student name: ", validate_name)
    age = ask("Age: ", validate_age)
    course = ask("Course (e.g. BCA): ", validate_course)
    marks = {}
    print("Enter marks out of 100:")
    for key, full_name, _ in SUBJECTS:
        marks[key] = ask(f"  {full_name}: ", validate_mark)
    student = manager.add_student(name, age, course, marks)
    print(f"Student added successfully with ID {student.student_id}.")


def display_all(manager):
    students = manager.all_students()
    if not students:
        print("No student records available.")
        return
    print()
    print_table(students)
    print(f"\nTotal students: {len(students)}")


def search_students(manager):
    keyword = input("Search by ID, name or course: ")
    results = manager.search(keyword)
    if not results:
        print("No matching students found.")
        return
    print()
    print_table(results)
    print(f"\n{len(results)} student(s) found.")


def update_student(manager):
    student = manager.get_student(input("Enter student ID to update: "))
    print(f"Current record: {student}")
    print("What do you want to update?\n1. Name\n2. Age\n3. Course\n4. Marks")
    choice = input("Choice: ").strip()

    if choice == "1":
        manager.update_details(student.student_id, name=ask("New name: ", validate_name))
    elif choice == "2":
        manager.update_details(student.student_id, age=ask("New age: ", validate_age))
    elif choice == "3":
        manager.update_details(student.student_id, course=ask("New course: ", validate_course))
    elif choice == "4":
        for i, (_, full_name, _) in enumerate(SUBJECTS, start=1):
            print(f"  {i}. {full_name}")
        pick = input("Subject number: ").strip()
        if not (pick.isdigit() and 1 <= int(pick) <= len(SUBJECTS)):
            print("Invalid subject number.")
            return
        key, full_name, _ = SUBJECTS[int(pick) - 1]
        manager.update_mark(student.student_id, key, ask(f"New marks for {full_name}: ", validate_mark))
    else:
        print("Invalid choice. Nothing was updated.")
        return
    print(f"Record updated: {student}")


def delete_student(manager):
    student = manager.get_student(input("Enter student ID to delete: "))
    print(f"Record: {student}")
    if input("Are you sure you want to delete this student? (y/n): ").strip().lower() == "y":
        manager.delete_student(student.student_id)
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def average_marks(manager):
    sid = input("Student ID (leave blank for whole class): ").strip()
    if sid:
        student = manager.get_student(sid)
        marks = student.marks
        print(f"\n{student.student_id} - {student.name} ({student.course})")
        for key, full_name, _ in SUBJECTS:
            print(f"  {full_name:<26}: {marks[key]}")
        print(f"  {'Average':<26}: {student.average():.2f}")
        print(f"  {'Result':<26}: {student.result()}")
        return

    class_avg = manager.class_average()
    if class_avg is None:
        print("No student records available.")
        return
    print("\nClass summary")
    for key, full_name, _ in SUBJECTS:
        print(f"  {full_name:<26}: {manager.subject_averages()[key]:.2f}")
    print(f"  {'Overall class average':<26}: {class_avg:.2f}")
    top = manager.topper()
    print(f"  {'Topper':<26}: {top.name} ({top.average():.2f})")


def save(manager):
    if manager.save_data():
        print("Records saved to students.csv.")


def main():
    manager = StudentManager()
    for msg in manager.load_data():
        print(msg)

    actions = {
        "1": add_student,
        "2": display_all,
        "3": search_students,
        "4": update_student,
        "5": delete_student,
        "6": average_marks,
        "7": save,
    }

    while True:
        print(MENU)
        choice = input("Enter your choice (1-8): ").strip()
        if choice == "8":
            save(manager)
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Please enter a number from 1 to 8.")
            continue
        try:
            action(manager)
        except (StudentNotFoundError, ValueError) as e:
            print(f"Error: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nInput cancelled.")


if __name__ == "__main__":
    main()
