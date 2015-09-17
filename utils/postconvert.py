import re
from os import listdir
from os import path

pattern = re.compile("<span.*?>(.*?)</span>")

basedir = "posts/"
outputdir = "output/"

def repl(match):
    return match.group(1)

def getFiles(directory):
    return [f for f in listdir(directory) if path.isfile(path.join(directory, f))]

def replaceContents(path):
    text = ""
    with open(basedir + path, 'r', encoding="utf8") as file:
        text = file.read()

    output = pattern.sub(repl, text)

    with open(outputdir + path, 'w', encoding="utf8") as file:
        file.write(output)

files = getFiles(basedir)

for file in files:
    replaceContents(file)

print("Done")
