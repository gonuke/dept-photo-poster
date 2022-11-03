import csv as csv
from pathlib import Path

with open('students.csv', newline='') as students:
    student_list = csv.reader(students)
    next(student_list)
    for student in student_list:
        Path('photos/' + student[0] + '_' + student[1] + '_' + student[2] + '.txt').touch()
