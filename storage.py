"""Load and save student data as JSON."""
import json
import os

from student import Student

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "students.json")


def load_students():
    """Return a dict {student_id: Student}. Empty if file missing/corrupt."""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("Warning: data file is corrupted. Starting with empty records.")
        return {}
    else:
        return {d["student_id"]: Student.from_dict(d) for d in raw}


def save_students(students):
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in students.values()], f, indent=2)
    except OSError as e:
        print(f"Error saving data: {e}")
        return False
    return True
