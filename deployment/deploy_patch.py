#!/bin/python
# -!- encoding:utf-8 -!-

# patch route in main.js -----------------------------------
content = ''
with open('src/static/js/main.js', 'r') as f:
    content = f.read()

content.replace('localhost:5000', 'mapif-insa.rhcloud.com')

with open('src/static/js/main.js', 'w') as f:
    f.write(content)
# ---------------------------------------------------------
