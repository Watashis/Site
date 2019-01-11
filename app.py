from flask import Flask
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from flask import send_file
import urllib.request
import json
import io

app = Flask(__name__, static_url_path='')


def database():
    with urllib.request.urlopen("http://shikimori.org/api/users/326282/anime_rates?limit=100000") as url:
        data = json.loads(url.read().decode())
        # print(data)
    # print(data[350])
    lists = (len(data)) - 1
    a = []
    i = 0
    plan = 0
    watching = 0
    completed = 0
    dropped = 0
    time = 0
    #print(data[i]['status'])
    while i <= lists:
        if data[i]['status'] == "planned":
            plan += 1
        if data[i]['status'] == "watching":
            watching += 1
            time += data[i]['episodes'] * 24
        if data[i]['status'] == "completed":
            completed += 1
            time += data[i]['episodes'] * 24
        if data[i]['status'] == "dropped":
            dropped += 1
        i += 1
    i = 0
    a.append(lists)
    a.append(plan)
    a.append(watching)
    a.append(completed)
    a.append(dropped)
    a = str(a[0])+'/'+str(a[1])+'/'+str(a[2])+'/'+str(a[3])+'/'+str(a[4]) + '\n' + 'Time: ' + str(time) + ' H'
    return a


def story():
    with urllib.request.urlopen("https://shikimori.org/api/users/326282/history?limit=30") as url:
        data = json.loads(url.read().decode())

    i = 0
    name = []
    while i <= (len(data) - 1):
        if (data[i]['description'])[:10] == 'Просмотрен':
            tmp = data[i]['target']['name']
            if len(tmp) > 23:
                name.append((tmp[:23] + '...'))
            else:
                name.append(data[i]['target']['name'])
        # print(data[i]['target']['name'])
        if len(name) == 4:
            break
        # print(data[i]['description'])
        i += 1
    # print(name)
    name = str(name[0]) + '\n' +str(name[1]) + '\n' +str(name[2]) + '\n' +str(name[3])
    return name


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
        
    font = ImageFont.truetype('6.otf', size=240)
    font2 = ImageFont.truetype('2.ttf', size=90)
    font1 = ImageFont.truetype('5.otf', size=190)
    color = (0, 0, 0, 0)
    image = Image.new('RGBA', (2000, 3000), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle(((0, 00), (2000, 3000)), fill="#40acfa")
    draw.rectangle(((25, 25), (1975, 2975)), fill="gray")
    draw.ellipse((28, 28, 1972, 1972), fill=(64, 172, 250, 255))
    size = (1900, 1900)
    im2 = Image.open('ava.JPG')
    im2 = crop(im2, size)
    im2.putalpha(prepare_mask(size, 4))
    image.paste(im2, (53, 53), im2)
    message = name
    bounding_box = [0, 1800, 2000, 2300]
    x1, y1, x2, y2 = bounding_box
    w, h = draw.textsize(message, font=font)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), message,  align='center', font=font)
    lists = database()
    history = story()
    bounding_box = [0, 2200, 1000, 2300]
    x1, y1, x2, y2 = bounding_box
    text = "List"
    w, h = draw.textsize(message, font=font1)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), text,  align='center', font=font1)

    bounding_box = [1000, 2200, 2000, 2300]
    x1, y1, x2, y2 = bounding_box
    text = "History"
    w, h = draw.textsize(message, font=font1)
    x = (x2 - x1 - w)/2 + x1
    y = (y2 - y1 - h)/2 + y1
    draw.text((x, y), text,  align='center', font=font1)
    text = history
    x = 1050
    y = 2380
    draw.text((x, y), text,  align='left', font=font2)
    text = lists
    x = 100
    y = 2380
    draw.text((x, y), text,  align='center', font=font2)
    size = imgsize
    if size != 0:
        basewidth = size
        wpercent = (basewidth/float(image.size[0]))
        hsize = int((float(image.size[1])*float(wpercent)))
        image = image.resize((basewidth, hsize), Image.ANTIALIAS)
    img_io = io.BytesIO()
    image.save(img_io, 'png', quality=90)
    img_io.seek(0)
    return img_io


@app.route("/")
def index():
    hui = '''<html xmlns="http://www.w3.org/1999/xhtml"><head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
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
    return hui


@app.route('/img/<site>/<int:size>')
def imgs(site, size):
    if site == 'shiki':
        img = image("Watashis",size,)
    else:
        img = image("Kanashina", size)
    return send_file(img, mimetype='image/png')



  # никуя не робит でも
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
