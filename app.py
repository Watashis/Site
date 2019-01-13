from flask import Flask
import PIL,urllib.request,json,io, textwrap,random, requests
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from flask import send_file
from flask import request

app = Flask(__name__, static_url_path='')

font, font1, font2, font3 = ImageFont.truetype('6.otf', size=240),ImageFont.truetype('5.otf', size=190),ImageFont.truetype('2.ttf', size=90), ImageFont.truetype('6.otf', size=30)

def prepare_mask(size, antialias=2):
    mask = Image.new('L', (size[0] * antialias, size[1] * antialias), 0)
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

def quotes_g(name, text, date, ava):
    def quote(info):
        color, bg, size = (0, 0, 0, 0), ['bg.png', 'bg1.png'], (200, 200)
        image = Image.new('RGBA', (700, 400), color)
        bg = random.choice(bg)
        im1 = Image.open(bg)
        im1, im2 = im1.resize([700, 400], Image.ANTIALIAS), Image.open(requests.get(info['ava'], stream=True).raw)
        im2 = crop(im2, size)
        im2.putalpha(prepare_mask(size, 4))
        im1.paste(im2, (20, 80), im2)
        image.paste(im1, [0, 0])
        draw, message = ImageDraw.Draw(image), info['text']
        a, i = textwrap.wrap(message, 40), 1
        message = a[0]
        while i <= (len(a) - 1):
            message += '\n' + a[i]
            i += 1
        x1, y1, x2, y2 = [250, 100, 650, 300]
        w, h = draw.textsize(message, font=font3)
        x, y, color2 = ((x2 - x1 - w)/2 + x1), ((y2 - y1 - h)/2 + y1), (0,0,0)
        if bg == 'bg1.png':
            color2 = (255,255,255)
        draw.text((x, y), message,  align='center', font=font3)
        text = '© {}\n@ {}'.format(info['name'], info['date'])
        draw.text((30, 300),  text, color2, align='left', font=font3)
        return image

    info = {"text": text,"name": name,'ava': ava,'date': date }
    img, img_io = quote(info), io.BytesIO()
    img.save(img_io, 'png', quality=90)
    img_io.seek(0)
    return img_io

def database():
    with urllib.request.urlopen("http://shikimori.org/api/users/326282/anime_rates?limit=100000") as url:
        data = json.loads(url.read().decode())
    a, i, time = [0, 0, 0, 0, 0], 0, 0
    a[0] = (len(data)) - 1
    while i <= a[0]:
        if data[i]['status'] == "planned":
            a[1] += 1
        if data[i]['status'] == "watching":
            a[2] += 1
        if data[i]['status'] == "completed":
            a[3] += 1
        if data[i]['status'] == "dropped":
            a[4] += 1
        time += data[i]['episodes']
        i += 1
    time = (time * 24) / 60
    a = '{}/{}/{}/{}/{}\nAll/P/W/C/D\nTime: {} H'.format(a[0], a[1], a[2], a[3], a[4], str(time))
    return a

def story():
    with urllib.request.urlopen("https://shikimori.org/api/users/326282/history?limit=30") as url:
        data = json.loads(url.read().decode())
    i, a = 0, []
    while i <= (len(data) - 1):
        if (data[i]['description'])[:10] == 'Просмотрен':
            tmp = data[i]['target']['name']
            if len(tmp) > 23:
                a.append((tmp[:23] + '...'))
            else:
                a.append(data[i]['target']['name'])
        if len(a) == 4:
            break
        i += 1
    a = '{}\n{}\n{}\n{}\n'.format(a[0], a[1], a[2], a[3])
    return a

def image(name, imgsize):
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
    lists = database()
    history = story()
    #history
    x1, y1, x2, y2 = historyB
    w, h = draw.textsize(history_T, font=font1)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), history_T,  align='center', font=font1)
    #list
    x1, y1, x2, y2 = listB
    w, h = 221, 227
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), lists_T,  align='center', font=font1)
    #listT
    x1, y1, x2, y2 = listTB
    w, h = draw.textsize(lists, font=font2)
    x,y = ((x2 - x1 - w)/2 + x1), 2467.0
    draw.text((x, y), lists,  align='center', font=font2)
    #historyT
    x1, y1, x2, y2 = historyTB
    w, h = draw.textsize(history, font=font2)
    x,y = ((x2 - x1 - w)/2 + x1), 2467.0
    draw.text((x, y), history,  align='center', font=font2)
    if size != 0:
        basewidth = imgsize
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    img_io = io.BytesIO()
    image.save(img_io, 'png', quality=90)
    img_io.seek(0)
    return img_io

@app.route("/")
def index():
    html = '''<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
    <meta http-equiv="Content-Type" content="text/html charset=UTF-8">
    <title>Типа сайт</title>
	<style>
	   .img {
	       position: fixed;
	       top: 50%;
	       left: 50%;
	       margin-top: -425;
	       margin-left: -425;
	   }
    </style>
    </head>
    <body>
    <div class="img">
		<img src="https://i.imgur.com/XNKiV4M.png">
	</div>
    </body></html>'''
    return html

@app.route("/quotes", methods=["POST"])
def test():
    name = request.form["name"]
    text = request.form["text"]
    date = request.form["data"]
    ava = request.form["ava"]
    return send_file(quotes_g(name, text, date, ava), mimetype='image/png')

@app.route('/test')
def Quote_test():
    name = 'People'
    text = 'Quote text'
    data = '2019-01-12'
    ava = 'https://i.imgur.com/ZxLbhil.jpg'
    return send_file(quotes_g(name, text, data, ava), mimetype='image/png')

@app.route('/img/<site>/<int:size>')
def imgs(site, size):
    img = image("Kanashina", size)
    if site == 'shiki':
        img = image("Watashis", size,)
    return send_file(img, mimetype='image/png')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
