import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def image(name, imgsize):
    def prepare_mask(size, antialias=2):
        mask = Image.new(
            'L', (size[0] * antialias, size[1] * antialias), 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + mask.size, fill=255)
        return mask.resize(size, Image.ANTIALIAS)

    def crop(im, s):
        w, h = im.size
        k = w / s[0] - h / s[1]
        if k > 0:
            im = im.crop(((w - h) / 2, 0, (w + h) / 2, h))
        elif k < 0:
            im = im.crop((0, (h - w) / 2, w, (h + w) / 2))
        return im.resize(s, Image.ANTIALIAS)

    font, font1, font2 = ImageFont.truetype('6.otf', size=240),ImageFont.truetype('5.otf', size=190),ImageFont.truetype('2.ttf', size=90)
    color,size = (0, 0, 0, 0), (1900, 1900)
    image = Image.new('RGBA', (2000, 3000), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle(((0, 00), (2000, 3000)), fill="#40acfa")
    draw.rectangle(((25, 25), (1975, 2975)), fill="gray")
    draw.ellipse((28, 28, 1972, 1972), fill=(64, 172, 250, 255))
    im2 = Image.open('ava.JPG')
    im2 = crop(im2, size)
    im2.putalpha(prepare_mask(size, 4))
    image.paste(im2, (53, 53), im2)

    #text
    history_T,lists_T = "History","List"
    #box
    bounding_box,historyB,listB,listTB,historyTB = [0, 1800, 2000, 2300], [1000, 2250, 2000, 2400],[0, 2250, 1000, 2400],[0, 2400, 1000, 3000],[1000, 2400, 2000, 3000]

    x1, y1, x2, y2 = bounding_box
    w, h = draw.textsize(name, font=font)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), name,  align='center', font=font)
    lists = '394/118/83/191/3\nAll/P/W/C/D\nTime: 1120.4 H'
    history = 'Another\nAnother\nYakusoku no Neverland\nTate no Yuusha no Naria...'

    #history
    x1, y1, x2, y2 = historyB
    w, h = draw.textsize(history_T, font=font1)
    print(w, h)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), history_T,  align='center', font=font1)

    #list
    x1, y1, x2, y2 = listB
    print(draw.textsize(lists_T, font=font1))
    w, h = 221, 227
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), lists_T,  align='center', font=font1)

    #listT
    x1, y1, x2, y2 = listTB
    w, h = draw.textsize(lists, font=font2)
    x = (x2 - x1 - w)/2 + x1
    y = ((y2 - y1 - h)/2 + y1) - 100
    draw.text((x, y), lists,  align='left', font=font2)

    #historyT
    x1, y1, x2, y2 = historyTB
    w, h = draw.textsize(history, font=font2)
    x = (x2 - x1 - w)/2 + x1
    y = ((y2 - y1 - h)/2 + y1) - 100
    draw.text((x, y), history,  align='left', font=font2)

    if size != 0:
        basewidth = imgsize
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    return image

image('Watashi',300).show()