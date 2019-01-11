import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw


def prepare_mask(size, antialias=2):
    mask = Image.new(
        'L', (size[0] * antialias, size[1] * antialias), 0)
    ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
    return mask.resize(size, Image.ANTIALIAS)

    # Обрезает и масштабирует изображение под заданный размер.
    # Вообще, немногим отличается от .thumbnail, но по крайней мере
    # у меня результат получается куда лучше.


def crop(im, s):
    w, h = im.size
    k = w / s[0] - h / s[1]
    if k > 0:
        im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
    elif k < 0:
        im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
    return im.resize(s, Image.ANTIALIAS)


# font = ImageFont.truetype('2.ttf', size=200)
font = ImageFont.truetype('6.otf', size=240)

font2 = ImageFont.truetype('2.ttf', size=90)

font1 = ImageFont.truetype('5.otf', size=190)

color = (0, 0, 0, 0)
image = Image.new('RGBA', (2000, 3000), color)
draw = ImageDraw.Draw(image)
# For easy reading

draw.rectangle(((0, 00), (2000, 3000)), fill="#40acfa")

draw.rectangle(((25, 25), (1975, 2975)), fill="gray")

draw.ellipse((28, 28, 1972, 1972), fill=(64, 172, 250, 255))
#draw.ellipse((53, 53, 1947, 1947), fill="gray")

size = (1900, 1900)
im2 = Image.open('ava.JPG')
im2 = crop(im2, size)
im2.putalpha(prepare_mask(size, 4))
print('')
print(im2.size)
print('')
image.paste(im2, (53, 53), im2)
#image.paste(im2, [0, 0])


message = 'Watashi'
bounding_box = [0, 1800, 2000, 2300]
x1, y1, x2, y2 = bounding_box  # For easy reading

# Calculate the width and height of the text to be drawn, given font size
w, h = draw.textsize(message, font=font)
# Calculate the mid points and offset by the upper left corner of the bounding box
x = (x2 - x1 - w)/2 + x1
y = (y2 - y1 - h)/2 + y1
# print(w, h)
# print(x, y)

# draw.rectangle([x1, y1, x2, y2])
draw.text((x, y), message,  align='center', font=font)
# draw.text((50, 200), message,  align='center', font=font)

# draw.text((300,2300), "Anime", (255,255,255), font=font1)
# draw.text((1280,2300), "TvShow", (255,255,255), font=font1)

# draw.text((50,2450), "300/150/40/10\nTime: 30 часов", (63,169,245), font=font2)
# draw.text((1030,2450), "300/150/40/10\nTime: 30 часов", (63,169,245), font=font2)
history = 'Another\nAnother\nYakusoku no Neverland\nTate no Yuusha no Naria...'

bounding_box = [0, 2200, 1000, 2300]
x1, y1, x2, y2 = bounding_box  # For easy reading
text = "List"
w, h = draw.textsize(message, font=font1)
x = (x2 - x1 - w)/2 + x1
y = (y2 - y1 - h)/2 + y1
print(w, h)
print(x, y)
# draw.rectangle([x1, y1, x2, y2])
draw.text((x, y), text,  align='center', font=font1)

bounding_box = [1000, 2200, 2000, 2300]
x1, y1, x2, y2 = bounding_box  # For easy reading
text = "History"
w, h = draw.textsize(message, font=font1)
x = (x2 - x1 - w)/2 + x1
y = (y2 - y1 - h)/2 + y1
print(w, h)
print(x, y)
# draw.rectangle([x1, y1, x2, y2])
draw.text((x, y), text,  align='center', font=font1)


text = history
x = 1050
y = 2380

draw.text((x, y), text,  align='left', font=font2)


text = "300/150/40/10\nTime: None H"
x = 100
y = 2380
draw.text((x, y), text,  align='center', font=font2)

# image.show()
image.save("static/test.png")
