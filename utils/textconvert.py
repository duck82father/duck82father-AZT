import os
import csv

cwd = os.getcwd()
file = os.path.join(cwd, 'python', 'src', 'congguksu_70108578583.txt')

with open(file, 'r', encoding='UTF8') as f:
    questions = []
    odd_even = 1

    for text in f:        
        text = text.strip()
        if text == "":
            continue
        elif odd_even == 1:
            sep_text = text.split('. ')
            odd_even = 0
        else :
            new_text = [sep_text[0], sep_text[1], text]
            questions += [new_text]
            odd_even = 1
            
    f.close()

print(questions)

azgag_file = file = os.path.join(cwd, 'python', 'src', 'azgag.csv')

with open(azgag_file, "w", newline="", encoding='UTF8') as file:
    writer = csv.writer(file)
    writer.writerows(questions)