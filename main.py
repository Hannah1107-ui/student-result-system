"""Student Result Management System - entry point and menu."""
import reports
import results
import storage
from student import Student, valid_dob, valid_id, MIN_SUBJECTS


def ask(prompt):
    return input(prompt).strip()


def ask_score(subject):
    """Keep asking until a score between 0 and 100 is entered."""
    while True:
        try:
            score = float(ask(f"  {subject} score (0-100): "))
        except ValueError: 
            print("  Please enter a number.")
            continue
        if 0 <= score <= 100:
            return score
        print("  Score must be between 0 and 100.")


def find(students, key):
    """Find by ID (exact) or by name (partial, case-insensitive)."""
    key_l = key.lower()
    return [s for s in students.values()
            if s.student_id.lower() == key_l or key_l in s.name.lower()]


def pick_student(students):
    matches = find(students, ask("Enter student ID or name: "))
    if not matches:
        print("No student found.")
        return None
    if len(matches) > 1:
        print("Multiple matches:")
        for s in matches:
            print(" ", s)
        sid = ask("Enter exact ID: ").upper()
        return students.get(sid)
    return matches[0]


def add_student(students):
    sid = ask("Student ID (e.g. STU001): ").upper()
    if not valid_id(sid):
        print("Invalid ID format. Use letters then digits, e.g. STU001.")
        return
    if sid in students:
        print("That ID already exists.")
        return
    name = ask("Full name: ")
    cls = ask("Class/Form: ")
    gender = ask("Gender (M/F): ").upper()
    dob = ask("Date of birth (YYYY-MM-DD): ")
    if not name or not cls or gender not in ("M", "F") or not valid_dob(dob):
        print("Invalid input. Student not added.")
        return
    students[sid] = Student(sid, name, cls, gender, dob)
    print("Student added. Remember to record scores (option 6).")


def view_students(students):
    if not students:
        print("No students registered.")
        return
    print(f"{'ID':<8} {'Name':<25} {'Class':<8} {'Gender':<7} DOB")
    for s in students.values():
        print(s)


def search_student(students):
    matches = find(students, ask("Search ID or name: "))
    if not matches:
        print("No match.")
    for s in matches:
        print(s)


def update_student(students):
    s = pick_student(students)
    if not s:
        return
    print("Leave blank to keep current value.")
    s.name = ask(f"Name [{s.name}]: ") or s.name
    s.class_name = ask(f"Class [{s.class_name}]: ") or s.class_name
    g = ask(f"Gender [{s.gender}]: ").upper()
    if g in ("M", "F"):
        s.gender = g
    dob = ask(f"DOB [{s.dob}]: ")
    if dob:
        if valid_dob(dob):
            s.dob = dob
        else:
            print("Invalid date ignored.")
    print("Student updated.")


def delete_student(students):
    s = pick_student(students)
    if s and ask(f"Delete {s.name}? (y/n): ").lower() == "y":
        del students[s.student_id]
        print("Deleted.")


def record_scores(students):
    s = pick_student(students)
    if not s:
        return
    print(f"Enter at least {MIN_SUBJECTS} subjects for {s.name}.")
    count = 0
    while True:
        subject = ask("Subject name (blank to finish): ")
        if not subject:
            if s.has_enough_scores():
                break
            print(f"  Need at least {MIN_SUBJECTS} subjects (have {len(s.scores)}).")
            continue
        s.set_score(subject, ask_score(subject))
        count += 1
    print("Scores saved.")


def update_score(students):
    s = pick_student(students)
    if not s or not s.scores:
        print("No scores to update.")
        return
    print("Subjects:", ", ".join(s.scores))
    subject = ask("Subject to update: ").title()
    if subject not in s.scores:
        print("Subject not found.")
        return
    s.set_score(subject, ask_score(subject))
    print("Score updated.")


def show_report_card(students):
    s = pick_student(students)
    if s and s.scores:
        print(reports.report_card(s))
    elif s:
        print("No scores recorded for this student.")


def list_results(students):
    scored = [s for s in students.values() if s.scores]
    if not scored:
        print("No results yet.")
        return
    choice = ask("Sort by (1) average or (2) name? ")
    ordered = results.sort_students(scored, "name" if choice == "2" else "average")
    print(reports.summary_table(ordered))


def show_stats(students):
    print(reports.stats_text(list(students.values())))


def save_report(students):
    scored = [s for s in students.values() if s.scores]
    if not scored:
        print("Nothing to report yet.")
        return
    try:
        print("Report saved to:", reports.save_report(scored))
    except OSError as e:
        print("Could not save report:", e)


MENU = """
===== STUDENT RESULT MANAGEMENT SYSTEM =====
 1. Add student            8. List all results
 2. View all students      9. Class statistics
 3. Search student        10. Save text report
 4. Update student         0. Save & exit
 5. Delete student
 6. Record scores
 7. Update a score
 R. Show report card
"""

ACTIONS = {"1": add_student, "2": view_students, "3": search_student,
           "4": update_student, "5": delete_student, "6": record_scores,
           "7": update_score, "r": show_report_card, "8": list_results,
           "9": show_stats, "10": save_report}


def main():
    students = storage.load_students()
    print(f"Loaded {len(students)} student(s).")
    while True:
        print(MENU)
        choice = ask("Choose an option: ").lower()
        if choice == "0":
            break
        action = ACTIONS.get(choice)
        if action is None:
            print("Invalid option.")
            continue
        try:
            action(students)
        except Exception as e:  # keep the program alive on unexpected errors
            print(f"Something went wrong: {e}")
        else:
            storage.save_students(students)
        finally:
            pass
    storage.save_students(students)
    print("Data saved. Goodbye!")


if __name__ == "__main__":
    main()
