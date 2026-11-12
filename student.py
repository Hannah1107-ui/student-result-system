"""Student class and validation helpers."""
import re
from datetime import datetime

ID_PATTERN = re.compile(r"^[A-Za-z]{2,4}\d{2,6}$")  # e.g. STU001
MIN_SUBJECTS = 5


def valid_id(student_id):
    return bool(ID_PATTERN.match(student_id))


def valid_dob(dob):
    """Return True if dob is a real date in YYYY-MM-DD format."""
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False


class Student:
    def __init__(self, student_id, name, class_name, gender, dob,
                 scores=None, result_date=None):
        self.student_id = student_id.upper()
        self.name = name
        self.class_name = class_name
        self.gender = gender
        self.dob = dob
        self.scores = scores if scores is not None else {}  # {subject: score}
        self.result_date = result_date  # date scores were last entered

    # ---- scores ----
    def set_score(self, subject, score):
        self.scores[subject.title()] = score
        self.result_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    def has_enough_scores(self):
        return len(self.scores) >= MIN_SUBJECTS

    # ---- (de)serialisation ----
    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "class_name": self.class_name,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "result_date": self.result_date,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(d["student_id"], d["name"], d["class_name"], d["gender"],
                   d["dob"], d.get("scores", {}), d.get("result_date"))

    def __str__(self):
        return (f"{self.student_id:<8} {self.name:<25} {self.class_name:<8} "
                f"{self.gender:<7} {self.dob}")
