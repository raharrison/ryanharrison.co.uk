import re
from os import listdir
from os import path

# pattern for matching content inside span tags
spanPattern = re.compile(r"<span.*?>(.*?)</span>")
# pattern for matching content inside Wordpress code tags
codePattern = re.compile(r"\[(.*?)\](.*?)\[\/\1?\]", re.DOTALL)

# base directory of markdown posts to convert
basedir = "../../ToConvert/"
# output directory for converted posts
outputdir = basedir + "output/"

# replace span tag with just it's contents
def replaceSpan(match):
    return '`' + match.group(1) + '`'

# repalce code tags with Jekyll highlighting
def replaceCode(match):
    # begin highlight, content, end highlight
    beginTag = r"{{% highlight {0} %}}".format(match.group(1))
    endTag = r"{% endhighlight %}"
    return "{0}{1}{2}".format(beginTag, match.group(2), endTag)

# retrive list of files in the specified directory
def getFiles(directory):
    return [f for f in listdir(directory) if path.isfile(path.join(directory, f))]

def convertPost(path):
    text = ""
    # read the post
    with open(basedir + path, 'r', encoding="utf8") as file:
        text = file.read()

    # replace span tags
    output = spanPattern.sub(replaceSpan, text)

    # replace code tags
    output = codePattern.sub(replaceCode, output)

    # output result
    with open(outputdir + path, 'w', encoding="utf8") as file:
        file.write(output)

files = getFiles(basedir)

for file in files:
    convertPost(file)

print("Converted " + str(len(files)) + " files")
