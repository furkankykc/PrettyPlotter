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
os.environ[ 'HOME' ] = '/tmp/'
matplotlib.use( 'Agg' )
from matplotlib import pyplot as plt

if not len(sys.argv) > 1:

    print("Content-Type: text/html")
    print()
    print('<meta name="viewport" content="width=device-width, initial-scale=1.0">')
    print('''
    
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>
   <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.6.0/dist/umd/popper.min.js" integrity="sha384-KsvD1yqQ1/1+IA7gi3P0tyJcT3vR+NdBTt13hSJ2lnve8agRGXTTyNaBYmCR/Nwi" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.min.js" integrity="sha384-nsg8ua9HAw1y0W1btsyWgBklPnCUAFLuTMS2G72MMONqmOymq585AcH49TLBQObG" crossorigin="anonymous"></script>
 <head>
  <title>Pretty Plotter</title>
  </head>
    ''')
    
    
    print('<body>')


def uploadForm():
    print("""
    <style>.checkbox-warning-filled [type="checkbox"][class*='filled-in']:checked+label:after {
  border-color: #FF8800;
  background-color: #FF8800;}
</style>
    <div class="container col-sm-4" >
<form enctype="multipart/form-data" action="save_file.py" method="post">

 

   <div class="form-control mb-3">
<label class="form-label" for="color">Plot Color</label>
<input id="color" class="form-control" type="color" name="color" value="#0433ff">
</div>
  <div class="form-floating mb-3">
<input id="limit" class="form-control" type="number" name="limit" value="-1" placeholder="-1" >
<label for="limit">Limit: </label>
   </div>
  <div class="form-check form-switch">
 <input id="cross" class="form-check-input" type="checkbox" name="cross" value="true" checked>
 <label class="form-check-label" for="cross">Merge</label>
   </div>
<div class="form-check form-switch">
<input class="form-check-input" id="legend" type="checkbox" name="legend" value="true" checked>
<label class="form-check-label" for="legend">Legends</label>
   </div>

<div class="form-check form-switch">
<input id="align" class="form-check-input" type="checkbox" name="align" value="true" checked>
<label class="form-check-label" for="align">Align</label>
   </div>
   <div class="form-check form-switch checkbox-warning-filled">
<input id="reset" class="form-check-input" type="checkbox" name="reset">
<label class="form-check-label" for="reset">Reset</label>
   </div>
   <div class="mb-3">
<label for="file">File: </label><input id="file" class="form-control form-control-sm" type="file" name="file" multiple="">
   </div>

<input class="form-control btn btn-primary" type="submit" value="Plot">
</div>
</div>
</form>""")

uploadForm()

if not len(sys.argv) > 1:
    print('</body>')

