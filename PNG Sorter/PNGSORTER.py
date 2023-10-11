import png
from PIL import Image
import Loader
from threading import Thread
import math
import random
from scipy.spatial import distance
import itertools
# CHANGE IMAGE PATHS FOR ANY 2 IMAGES OF THE SAME AMOUNT OF PIXELS
r = png.Reader(filename = "pic1.png")
r2 = png.Reader(filename = "pic2.png")
colors = []
colors2 = []
ordered = []
ordered2 = []

#sorts into groups of 4: R,G,B,A
def order(vals):
    final = []
    for l in vals:
        Loader.iterator += 1
        for i in range(0, len(l), 4):
            final.append(l[i:i+4])
    return final

#OPTIONAL : Writes RGBA pixels to a file
#def write(o):
#    f = open("test.txt", "w")
#    for r in o:
#        f.write(str(r) + "\n")
#    f.close()

def FindColors(ordered, ordered2):
        currentSet = [o for o in ordered]
        replacers2 = [None for i in range(len(ordered2))]
        for c in range(len(ordered2)):
            x = sort(currentSet, ordered2[c])
            replacers2[c] = currentSet[x]
            currentSet.pop(x)
            Loader.iterator += 1
        return replacers2
#Print an image goin pixel-by-pixel
def Print(imge, clrs):
    image = imge
    width = image[0]
    height = image[1]
    rgba_values = clrs
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    pixels = img.load()
    for y in range(height):
        for x in range(width):
            rgba = rgba_values[(y * width) + x]
            pixels[x, y] = tuple(rgba)
    img.save("Output"+".png")

#Find closest color in a list of colors
def sort(clrs, cc):
    closest_index = distance.cdist([cc], clrs).argmin()
    Loader.iterator +=1
    return closest_index
def Main():
    #grab global variables
    global colors
    global colors2
    global ordered
    global ordered2
    #read images
    image = r.read()
    image2 = r2.read()
    #make list of values for each image
    rgbvals = [[a for a in i ]for i in image[2]]
    rgbvals2 = [[a for a in i ]for i in image2[2]]
    #order images
    Loader.setLoader(len(rgbvals), "ordering 1st image")
    ordered = order(rgbvals)
    Loader.setLoader(len(rgbvals2), "ordering 2nd image")
    ordered2 = order(rgbvals2)
    #find closest colors
    Loader.setLoader(len(ordered), "finding equivalent colors for image")
    replacers2 = FindColors(ordered,ordered2)
    Loader.setLoader(len(ordered), "writing image")
    final=[]
    #set replaced colors in order with pixels
    for c in ordered:
        final.append(replacers2[ordered.index(c)])
        Loader.iterator +=1
    #print
    Print(image, final)
    Loader.stop = True
Loader.startLoader()
Main()
print("DONE!!!! Saved as 'Output.png'. ")
