import PIL
from PIL import Image
import numpy as np
import os

MASK = "blank.png"
DATA = "something.bin"
OUT = "org2.png"
#MASK = "eyes_no_white.png"
#DATA = "secret.ogg"
#OUT = "out.png"
OUTDATA = OUT + ".bin"

maskimg = Image.open(MASK)

with open(DATA, "rb") as f:
	data = f.read()
outimg = Image.new(mode="RGBA", size=(maskimg.width, maskimg.height), color=(0,0,0,0))

pos = 0
for y in range(maskimg.height):
	for x in range(maskimg.width):
		pixel = maskimg.getpixel((x,y))
		if pixel[3] > 0: # check alpha
			outimg.putpixel((x,y), pixel)
			continue
		idx = pos // 8
		if idx >= len(data):
			outimg.putpixel((x,y), (0,0,0,0))
			continue
		byte = data[idx]
		num = 255 if (1 & (byte >> (7-(pos % 8)))) else 0
		outimg.putpixel((x,y), (num,num,num,69))
		pos += 1
outimg.save(OUT, compress_level=9)
outimg.close()
os.system(f"pngcrush -ow {OUT}")


inimg = Image.open(OUT)
s = ""
for y in range(inimg.height):
	for x in range(inimg.width):
		pixel = inimg.getpixel((x,y))
		if pixel[3] != 69:
			continue
		if pixel[0] > 0:
			s += "1"
		else:
			s += "0"

i = 0
buffer = bytearray()
while i < len(s):
	buffer.append( int(s[i:i+8], 2) )
	i += 8

with open(OUTDATA, 'wb') as f:
	f.write(buffer)
