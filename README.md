# Student Result Management System

A menu-driven Python app for managing student records, scores, grades and reports in a secondary school.

## Features
- Add, view, search, update and delete students
- Record 5+ subject scores, auto total / average / grade
- Report cards, sorted result lists, class statistics
- Save text reports to `reports/`
- JSON persistence in `data/students.json` 

## Run
Requires Python 3.8+ (standard library only).

    python main.py

## Structure
| File | Purpose |
|------|---------|
| main.py | Menu and user interaction |
| student.py | `Student` class, regex/date validation |
| results.py | Total, average, grading, sorting, stats |
| storage.py | Load/save JSON |
| reports.py | Report card and text report generation |

## Grading
A: 70+ | B: 60-69 | C: 50-59 | D: 45-49 | F: below 45

## Python concepts used
Variables and type conversion, if/elif/else, loops, lists/dicts/tuples,
functions, sorting, try/except/else/finally, file I/O (JSON), modules,
OOP (Student class), datetime, regex, `os`/`json` standard library.

## Confirmation that the project runs without major errors
The program runs without major errors. All features (add, view, search, update and delete students, record scores, reports, and saving/loading data) were tested and work correctly.
