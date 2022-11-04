import csv
from pathlib import Path
import glob

with open('students.csv', newline='') as students:
    student_list = csv.reader(students)
    next(student_list)
    for student in student_list:
        # print(glob.glob("photos/" + student[0] + '*'))
        if len(glob.glob("photos/" + student[0] + '*')) < 1:
            # print("adding: ", student)
            Path('photos/' + student[0] + '_' + student[1] + '_' + student[2] + '.txt').touch()
        else:
            pass # print("skipping: ", student)
