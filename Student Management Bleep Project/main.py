# main.py
# Student Management System - menu driven console program

from manager import StudentManager
from student import SUBJECTS, SUBJECT_NAMES, validate_name, validate_age, validate_mark, validate_course


def show_menu():
    print()
    print("========== STUDENT MANAGEMENT SYSTEM ==========")
    print("1. Add student")
    print("2. Display all students")
    print("3. Search students")
    print("4. Update student record")
    print("5. Delete student")
    print("6. Calculate average marks")
    print("7. Save records")
    print("8. Save and exit")
    print("================================================")


def ask(prompt, validate_func):
    # keep asking until the value passes the validation function
    while True:
        value = input(prompt)
        try:
            return validate_func(value)
        except ValueError as e:
            print("  Invalid input:", e)


def print_table(students):
    header = "ID".ljust(7) + "Name".ljust(23) + "Age".ljust(5) + "Course".ljust(9)
    for sub in SUBJECTS:
        header = header + SUBJECT_NAMES[sub][:6].rjust(7)
    header = header + "Avg".rjust(8) + "  Result"
    print(header)
    print("-" * (len(header) + 6))

    for s in students:
        marks = s.get_marks()
        row = (s.get_id().ljust(7) + s.get_name()[:22].ljust(23)
               + str(s.get_age()).ljust(5) + s.get_course().ljust(9))
        for sub in SUBJECTS:
            row = row + str(marks[sub]).rjust(7)
        row = row + format(s.get_average(), "8.2f") + "  " + s.get_result()
        print(row)


def add_student(mgr):
    name = ask("Student name: ", validate_name)
    age = ask("Age: ", validate_age)
    course = ask("Course (e.g. BCA): ", validate_course)

    marks = {}
    print("Enter marks out of 100:")
    for sub in SUBJECTS:
        marks[sub] = ask("  " + SUBJECT_NAMES[sub] + ": ", validate_mark)

    s = mgr.add_student(name, age, course, marks)
    print("Student added successfully with ID", s.get_id())


def display_all(mgr):
    students = mgr.get_all()
    if len(students) == 0:
        print("No student records available.")
        return
    print()
    print_table(students)
    print("\nTotal students:", len(students))


def search_students(mgr):
    keyword = input("Search by ID, name or course: ")
    results = mgr.search(keyword)
    if len(results) == 0:
        print("No matching students found.")
        return
    print()
    print_table(results)
    print("\n" + str(len(results)) + " student(s) found.")


def update_student(mgr):
    s = mgr.find_student(input("Enter student ID to update: "))
    print("Current record:", s)
    print("What do you want to update?")
    print("1. Name")
    print("2. Age")
    print("3. Course")
    print("4. Marks")
    choice = input("Choice: ").strip()

    if choice == "1":
        mgr.update_details(s.get_id(), name=ask("New name: ", validate_name))
    elif choice == "2":
        mgr.update_details(s.get_id(), age=ask("New age: ", validate_age))
    elif choice == "3":
        mgr.update_details(s.get_id(), course=ask("New course: ", validate_course))
    elif choice == "4":
        count = 1
        for sub in SUBJECTS:
            print(" ", count, "-", SUBJECT_NAMES[sub])
            count += 1
        pick = input("Subject number: ").strip()
        if not pick.isdigit() or int(pick) < 1 or int(pick) > len(SUBJECTS):
            print("Invalid subject number.")
            return
        sub = SUBJECTS[int(pick) - 1]
        new_marks = ask("New marks for " + SUBJECT_NAMES[sub] + ": ", validate_mark)
        mgr.update_mark(s.get_id(), sub, new_marks)
    else:
        print("Invalid choice. Nothing was updated.")
        return

    print("Record updated:", s)


def delete_student(mgr):
    s = mgr.find_student(input("Enter student ID to delete: "))
    print("Record:", s)
    confirm = input("Are you sure you want to delete this student? (y/n): ")
    if confirm.strip().lower() == "y":
        mgr.delete_student(s.get_id())
        print("Student deleted.")
    else:
        print("Deletion cancelled.")


def average_marks(mgr):
    sid = input("Student ID (leave blank for whole class): ").strip()

    if sid != "":
        s = mgr.find_student(sid)
        marks = s.get_marks()
        print()
        print(s.get_id(), "-", s.get_name(), "(" + s.get_course() + ")")
        for sub in SUBJECTS:
            print("  " + SUBJECT_NAMES[sub].ljust(26) + ":", marks[sub])
        print("  " + "Average".ljust(26) + ":", format(s.get_average(), ".2f"))
        print("  " + "Result".ljust(26) + ":", s.get_result())
        return

    avg = mgr.class_average()
    if avg is None:
        print("No student records available.")
        return

    print("\nClass summary")
    subj_avg = mgr.subject_averages()
    for sub in SUBJECTS:
        print("  " + SUBJECT_NAMES[sub].ljust(26) + ":", format(subj_avg[sub], ".2f"))
    print("  " + "Overall class average".ljust(26) + ":", format(avg, ".2f"))
    top = mgr.topper()
    print("  " + "Topper".ljust(26) + ":", top.get_name(), "(" + format(top.get_average(), ".2f") + ")")


def save(mgr):
    if mgr.save_data():
        print("Records saved to students.csv.")


def main():
    mgr = StudentManager()
    for msg in mgr.load_data():
        print(msg)

    while True:
        show_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == "8":
            save(mgr)
            print("Goodbye!")
            break

        try:
            if choice == "1":
                add_student(mgr)
            elif choice == "2":
                display_all(mgr)
            elif choice == "3":
                search_students(mgr)
            elif choice == "4":
                update_student(mgr)
            elif choice == "5":
                delete_student(mgr)
            elif choice == "6":
                average_marks(mgr)
            elif choice == "7":
                save(mgr)
            else:
                print("Invalid choice. Please enter a number from 1 to 8.")
        except ValueError as e:
            print("Error:", e)
        except Exception as e:
            print("Error:", e)
        except KeyboardInterrupt:
            print("\nInput cancelled.")


if __name__ == "__main__":
    main()
