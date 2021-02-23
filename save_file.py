#!/usr/bin/python3
import sys
import matplotlib
import os
import cgi
import cgitb
from Bio import Entrez
import re
import pickle
import numpy as np
import subprocess
import pandas as pd

cgitb.enable()
matplotlib.use('Agg')
from matplotlib import pyplot as plt

# my_path = os.getcwd() 
my_path = os.path.join(os.getcwd(),
                       'data')  # Figures out the absolute path for you in case your working directory moves around.

# Figures out the absolute path for you in case your working directory moves around.
if not len(sys.argv) > 1:
    print("Content-Type: text/html")
    print()
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('''<!-- Latest compiled and minified CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">

    <!-- Optional theme -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous">

    <!-- Latest compiled and minified JavaScript -->
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>''')
    print('<body>')
    print(
        '''
        <div class="container">
  <div class="jumbotron">
    <h1>Plot Results</h1>
    <a href=\"plotter.py\">Go Back</a>
  </div>

  <div class="row .no-gutters" >
        '''
    )

form = cgi.FieldStorage()
filefield = None
# A nested FieldStorage instance holds the file
if 'file' in form:
    filefield = form['file']
message = ""
if not isinstance(filefield, list):
    filefield = [filefield]
# Test if the file was uploaded
uploadFolder = my_path
for fileitem in filefield:
    if fileitem is not None:
        if fileitem.filename:
            # strip leading path from file name
            # to avoid directory traversal attacks
            fn = os.path.basename(fileitem.filename.replace("\\", "/"))
            open(os.path.join(uploadFolder, fn), 'wb').write(fileitem.file.read())
            # print('The file "' + fn + '" was uploaded successfully')


def showPlot(my_file, ax=None, label=False, inverted=False):
    myfullpath = os.path.join(my_path, my_file)
    # myfullpath = '/Users/furkankykc/Sites/ex1.png'
    if (os.path.isfile(myfullpath)):
        os.remove(myfullpath)
    if inverted:
        plt.gca().invert_yaxis()
    plt.savefig(myfullpath, dpi=300)
    print('''
    <div class="col-sm-6">
    
    ''')
    if label:
        print(f"<h3>{my_file.split('.')[0]} Plot </h3>")

    print("<img width=\"400\" class=\"w-100\" height=\"300\"src=\"data/" + my_file + ".png\">")
    print('''
</div>''')


def dataalign(path, align=True, lim=-1, sep=' ', ax=None, color=None, text_size=12):
    data = np.loadtxt(path, delimiter=sep, dtype=np.float, skiprows=2)
    lab = read_label(path)
    x, y = data.T
    if align:
        x = x - min(x)
    if lim != -1:
        x = x[np.where(x < lim)]
    if color is not None:
        if ax is None:
            plt.plot(x, y[:len(x)], label=lab.split("|")[3], color=color)
        else:
            ax.plot(x, y[:len(x)], label=lab.split("|")[3], color=color)
    else:
        if ax is None:
            plt.plot(x, y[:len(x)], label=lab.split("|")[3])
        else:
            ax.plot(x, y[:len(x)], label=lab.split("|")[3])
    if label_x is not None:
        plt.xlabel(label_x, fontweight='bold', size=text_size)
    if label_y is not None:
        plt.ylabel(label_y, fontweight='bold', size=text_size)
    plt.xticks(weight='bold', size=text_size)
    plt.yticks(weight='bold', size=text_size)


def read_label(file):
    arr = []
    with open(file) as file_data:
        for line in file_data.readlines()[0:2]:
            arr.append(line.replace('\n', ''))
            arr.append(file.split('/')[-1].split('.')[0])
        # print('\n'.join(arr))
    return '|'.join(arr)


def removeFiles():
    for root, dirs, files in os.walk(my_path):
        for file in files:
            if file.lower().endswith('.txt'):
                os.remove(os.path.join(my_path, file))


def plot(cross=False, legend=False, align=False, limit=-1, color='blue', inverted=False, text_size=12):
    import os
    if cross:
        fig, ax = plt.subplots(figsize=(8, 6))
    filetype = '.txt'
    for root, dirs, files in os.walk(my_path):
        for file in files:
            if file.lower().endswith(filetype.lower()):
                if legend:
                    plt.legend()
                if not cross:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    dataalign(os.path.join(root, file), align=align, lim=limit, ax=ax, color=color, text_size=text_size)

                    showPlot(file.split('.')[0], label=True, inverted=inverted)
                else:
                    dataalign(os.path.join(root, file), align=align, lim=limit, ax=ax, text_size=text_size)

    if cross:
        print("""<h3>Crossed Plot</h3>""")
        showPlot('temp4', inverted=inverted)


legend = form.getvalue('legend')
cross = form.getvalue('cross')
reset = form.getvalue('reset')
align = form.getvalue('align')
color = form.getvalue('color')
limit = int(form.getvalue('limit'))
label_x = form.getvalue('xlabel')
label_y = form.getvalue('ylabel')
inverted = form.getvalue('invert')
text_size = int(form.getvalue('size'))

if limit is None:
    limit = -1
if label_y is None:
    label_y = 'Current(V)'
if label_x is None:
    label_x = 'Time(s)'
if text_size is not None:
    text_size = 12
if reset:
    removeFiles()
else:
    fig, ax = plt.subplots(figsize=(8, 6))

    plt.xticks(weight='bold', size=text_size)
    plt.yticks(weight='bold', size=text_size)
    plt.ylabel(label_y, fontweight='bold', size=text_size)
    plt.xlabel(label_y, fontweight='bold', size=text_size)
    plot(cross, legend, align, limit, color, inverted, text_size=text_size)
if not len(sys.argv) > 1:
    print('</body>')

# form = cgi.FieldStorage()
# if 'file' in form:
#     print('File in form')
#     filefield = form['file']
#     if not isinstance(filefield, list):
#         filefield = [filefield]

#     for fileitem in filefield:
#         if fileitem.filename:
#             # save file
#             fn = os.path.basename(fileitem.filename.replace("\\", "/" ))
#             print(fn)
#             open(os.path.join(uploadFolder,fn), 'wb').write(fileitem.file.read())
# print("Location: cgi-bin/plotter.py")

print('''</div>
''')
print("</body>")
# cgi.redirect('cgi-bin/plotter.py')
