#!/usr/bin/env python

import glob
from string import Template

photos_per_row = 13
photo_table_column_format = 'c' * (2 * photos_per_row - 1)
photo_width = "4in"
column_padding = "1cm"

paper_width = "72in"
paper_height = "48in"
text_width = "70in"
text_height = "46in"
logo_width = "12in"
title_font_size = "2.5in"
title_font_lineheight = "2.7in"
name_font_size = "1cm"
name_font_lineheight = "1.2cm"
missing_font_size = "1.5cm"
missing_font_lineheight = "1.7cm"

document_tmpl = Template("""\\documentclass[12pt]{article}

\\usepackage[papersize={$paper_width,$paper_height}, width=$text_width, height=$text_height]{geometry}
\\usepackage{graphicx}
\\usepackage{txfonts}

\\begin{document}
\\begin{center}
    \\fontsize{$title_font_size}{$title_font_lineheight}\\selectfont 
    \\begin{tabular}{cl}
      \\begin{tabular}{c} \\includegraphics[width=$logo_width]{ep-logo} \\end{tabular} &
      \\begin{tabular}{c} Graduate Student Community \\end{tabular}
    \\end{tabular}

    \\fontsize{$name_font_size}{$name_font_lineheight}\\selectfont 
    \\begin{tabular}{cc}
      \\begin{tabular}{$photo_table_column_format} $photo_table_contents \\end{tabular} &
      \\fontsize{$missing_font_size}{$missing_font_lineheight}\\selectfont 
      \\begin{tabular}{c} $missing_list_contents \\end{tabular}
    \\end{tabular}  
\\end{center}
\\end{document}""")

def build_photo_table(photos_per_row, photo_width, column_padding):

    photo_file_list = []
    for fmt in ["jpg", "jpeg", "png"]:
        photo_file_list.extend(glob.glob("photos/*." + fmt))
    photo_file_list.sort()

    num_photos = len(photo_file_list)

    photo_table_contents = ""
    rows = []

    for row_start in range(0, num_photos, photos_per_row):
        photo_row = []
        label_row = []
        for idx in range(row_start, min(row_start + photos_per_row, num_photos)):
            filename = photo_file_list[idx]
            photo_row.append("        \\includegraphics[width=" + photo_width + "]{" + filename + "}" )
            label_row.append("        " + make_name(filename))
        rows.extend(['&\\hspace*{1.5cm}&\n'.join(photo_row), ('&\\hspace*{' + column_padding + '}&\n').join(label_row)])
    photo_table_contents += "\\\\\n".join(rows)

    return photo_table_contents

def make_name(filename):

    name_parts = filename.split('.')[0].split('/')[1].split('_')
    return ' '.join([name_parts[1], name_parts[0], "("+name_parts[2]+")"])

def build_missing_list():

    missing_student_list = glob.glob("photos/*.txt")
    missing_student_list.sort()

    missing_list_contents = "\\underline{Not Pictured}"

    for filename in missing_student_list:
        missing_list_contents += "\\\\\n         " + make_name(filename) 

    return missing_list_contents


photo_table_contents = build_photo_table(photos_per_row, photo_width, column_padding)
missing_list_contents = build_missing_list()

document = document_tmpl.substitute(paper_width = paper_width,
    paper_height = paper_height,
    text_width = text_width,
    text_height = text_height,
    title_font_size = title_font_size,
    title_font_lineheight = title_font_lineheight,
    logo_width = logo_width,
    name_font_size = name_font_size,
    name_font_lineheight = name_font_lineheight,
    missing_font_size = missing_font_size,
    missing_font_lineheight = missing_font_lineheight,
    photo_table_column_format = photo_table_column_format,
    photo_table_contents = photo_table_contents,
    missing_list_contents = missing_list_contents) 


with open("poster.tex", "w") as poster_file:
    poster_file.write(document)
