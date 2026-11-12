"""Report generation functions."""
import os
from datetime import datetime

import results

LINE = "=" * 62


def report_card(student):
    avg = results.average(student)
    lines = [LINE, "STUDENT REPORT CARD".center(62), LINE,
             f"ID     : {student.student_id}",
             f"Name   : {student.name}",
             f"Class  : {student.class_name}    Gender: {student.gender}",
             f"DOB    : {student.dob}",
             f"Result entered: {student.result_date or 'N/A'}",
             "-" * 62, f"{'Subject':<30}{'Score':>10}", "-" * 62]
    for subject, score in student.scores.items():
        lines.append(f"{subject:<30}{score:>10.1f}")
    lines += ["-" * 62,
              f"{'Total':<30}{results.total(student):>10.1f}",
              f"{'Average':<30}{avg:>10.2f}",
              f"{'Grade':<30}{results.grade(avg):>10}", LINE]
    return "\n".join(lines)


def summary_table(students):
    lines = [f"{'ID':<8}{'Name':<25}{'Total':>8}{'Average':>10}{'Grade':>7}",
             "-" * 58]
    for s in students:
        avg = results.average(s)
        lines.append(f"{s.student_id:<8}{s.name:<25}{results.total(s):>8.1f}"
                     f"{avg:>10.2f}{results.grade(avg):>7}")
    return "\n".join(lines)


def stats_text(students):
    stats = results.class_stats(students)
    if stats is None:
        return "No scores recorded yet."
    high, low, avg = stats
    return (f"Highest average : {high:.2f}\n"
            f"Lowest average  : {low:.2f}\n"
            f"Class average   : {avg:.2f}")


def full_report(students):
    ordered = results.sort_students(students, "average")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return "\n".join([LINE, "CLASS RESULT REPORT".center(62),
                      f"Generated: {now}".center(62), LINE,
                      summary_table(ordered), "", "CLASS STATISTICS",
                      "-" * 20, stats_text(students)])


def save_report(students, filename=None):
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports")
    os.makedirs(folder, exist_ok=True)
    if not filename:
        filename = datetime.now().strftime("report_%Y%m%d_%H%M%S.txt")
    path = os.path.join(folder, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(full_report(students))
    return path
