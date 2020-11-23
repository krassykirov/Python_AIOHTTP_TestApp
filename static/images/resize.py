from PIL import Image
import glob

size = 512,512

files = glob.glob("./*.jpg")
for file in files:
    im = Image.open(file)
    print(file,im.size)
    im.size(size)
    im.save(file + ".jpg")