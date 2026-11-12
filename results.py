"""Score calculation and grading logic."""


def total(student):
    return sum(student.scores.values())


def average(student):
    if not student.scores:
        return 0.0
    return total(student) / len(student.scores)


def grade(avg):
    if avg >= 70:
        return "A"
    elif avg >= 60:
        return "B"
    elif avg >= 50:
        return "C"
    elif avg >= 45:
        return "D"
    return "F"


def sort_students(students, by="average"):
    """Sort by 'average' (highest first) or 'name' (A-Z)."""
    if by == "name":
        return sorted(students, key=lambda s: s.name.lower())
    return sorted(students, key=average, reverse=True)


def class_stats(students):
    """Return (highest, lowest, class_average) over student averages,
    or None if nobody has scores."""
    avgs = [average(s) for s in students if s.scores]
    if not avgs:
        return None
    return max(avgs), min(avgs), sum(avgs) / len(avgs)
