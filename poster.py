#!/usr/bin/env python

import glob

photos_per_row = 3
photo_width = "5in"
table_header = "\\begin{tabular}{" + "c" * (2 * photos_per_row - 1) + "}"
table_footer = "\\end{tabular}"
document_header = """\\documentclass[12pt]{article}

\\usepackage[papersize={72in,36in}, width=70in, height=34in]{geometry}
\\usepackage{graphicx}
\\usepackage{txfonts}

\\begin{document}
\\begin{center}
    \\fontsize{2.5in}{2.5in}\\selectfont 
    \\begin{tabular}{cl}
    \\begin{tabular}{c}\\includegraphics[width=12in]{ep-logo}\\end{tabular} &
    \\begin{tabular}{c}Graduate Student Community\\end{tabular}
    \\end{tabular}

    \\fontsize{1cm}{1cm}\\selectfont """
document_footer = """
\\end{center}

\\end{document}"""

photo_file_list = glob.glob("photos/*.jpeg")
photo_file_list.sort()

student_data = []
for filename in photo_file_list:
    name_parts = filename.split('.')[0].split('/')[1].split('_')
    student_data.append((' '.join([name_parts[1], name_parts[0], "("+name_parts[2]+")"]), filename))

table_contents = ""
rows = []
for row_start in range(0, len(student_data), photos_per_row):
    photo_row = []
    label_row = []
    for idx in range(row_start, min(row_start + photos_per_row,len(student_data))):
        photo_row.append("    \\includegraphics[width=" + photo_width + "]{" + student_data[idx][1] + "}")
        label_row.append("    " + student_data[idx][0] )
    rows.extend(['&\\hspace*{1.5cm}&\n'.join(photo_row), '&\\hspace*{1.5cm}&\n'.join(label_row)])
table_contents += "\\\\\n".join(rows)

with open("poster.tex", "w") as poster_file:
    poster_file.write("\n".join([document_header, table_header, table_contents, table_footer, document_footer]))

