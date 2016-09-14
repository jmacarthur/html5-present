#!/usr/bin/env python2

from HTMLParser import HTMLParser
import os
import shutil
import sys

outputDir = "output"
slideNumber = 0
outputfile = None
inSlide = False
inputDirectory = None

standardHeader = """
<html>
<head>
<link rel="stylesheet" type="text/css" href="presentation.css">
<body>
<div class="scaleable-wrapper" id="scaleable-wrapper">
<div class="slide-contents" id="slide-contents">
"""

standardFooter = """
</div></div>
</body>
</html>
"""

def makeNavigation(currentSlideNo, lastSlide = False):
    if currentSlideNo > 1:
        navigateLeft = "window.location.href = 'slide%d.html';"%(currentSlideNo-1)
    else:
        navigateLeft = "// First slide"
    if lastSlide:
        navigateRight = "// Last slide"
    else:
        navigateRight = "window.location.href = 'slide%d.html';"%(currentSlideNo+1)

    javascript = """<script>
    document.onkeydown = checkKey;
    function checkKey(e) {
      e = e || window.event;
      if (e.keyCode == '37') {
         %s
         console.log("left");
      }
      else if (e.keyCode == '39') {
         %s
         console.log("right");
      }
      else if (e.keyCode == 32) {
          e.preventDefault();
          var video = document.getElementById("Video1");
           if (video.paused) {
             video.play();
           } else {
             video.pause();
           }
      }
    }
    </script>
    <script src="resizer.js"></script>
    """ % (navigateLeft, navigateRight)
    return javascript

def finishSlide(outputFile, slideNo, lastSlide = False):
    outputFile.write(makeNavigation(slideNumber, lastSlide))
    outputFile.write(standardFooter)
    outputFile.close()

def format_tag(tag, attrs):
    if attrs==[]:
        return "<%s>"%tag
    attrText = []
    for k in attrs:
        attrText.append("%s=\"%s\""%(k,attrs[k]))
    return "<%s %s>"%(tag, " ".join(attrText))

# create a subclass and override the handler methods
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global slideNumber, outputfile, inSlide
        attrs=dict(attrs)
        print("Encountered a start tag:", tag)
        if(tag=='slide'):
            if outputfile is not None: finishSlide(outputfile, slideNumber)
            inSlide = True
            slideNumber += 1
            outputfile = open(os.path.join(outputDir,"slide%d.html"%(slideNumber)),"wt")
            outputfile.write(standardHeader)
            return
        elif(tag=='video'):
            if not 'id' in attrs:
                attrs["id"] = "Video1"
        elif(tag=='source'): # Used by 'video'
            filename = attrs["src"]
            self.copyFile(filename)
        elif(tag=='img'):
            filename = attrs["src"]
            self.copyFile(filename)
        outputfile.write(format_tag(tag,attrs))

    def copyFile(self, filename):
        sourceFile = os.path.join(inputDirectory, filename)
        if os.path.exists(sourceFile):
            shutil.copyfile(sourceFile, os.path.join(outputDir,filename))
        else:
            print("Source image %s does not exist"%filename)
            exit(1)

    def handle_endtag(self, tag):
        global slideNumber, outputfile, inSlide
        print("Encountered an end tag :", tag)
        if(tag=='slide'):
            inSlide = False
        else:
            outputfile.write("</%s>"%tag)
    def handle_data(self, data):
        global outputfile, inSlide
        if inSlide:
            outputfile.write(data)
        else:
            print("Encountered some data outside a slide tag:", data)

def main():
    global outputfile, slideNumber, inputDirectory
    if len(sys.argv) != 2:
        print("Usage: convert.py example.html")
        exit(1)

    inputFilename = sys.argv[1]
    (inputDirectory, _) = os.path.split(inputFilename)
    f = open(inputFilename)
    html = f.read()
    f.close()
    if not os.path.exists(outputDir):
        os.mkdir(outputDir)
    elif not os.path.isdir(outputDir):
        print("Output path '%s' exists but isn't a directory; can't continue")
        sys.exit(1)
    for i in ["presentation.css","resizer.js"]:
        shutil.copyfile(i, os.path.join(outputDir,i))
    # instantiate the parser and fed it some HTML
    parser = MyHTMLParser()
    parser.feed(html)
    finishSlide(outputfile, slideNumber, lastSlide = True)
    print("Conversion complete. You can view your presentation at:")
    print("file://%s/slide1.html" % os.path.abspath(outputDir))

if __name__=="__main__":
    main()
