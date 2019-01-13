# Example of collaboration between Flask and PIL
- The site is able to generate images with text.
  - At the moment, the site can generate 2 image.
    1. card with profile information of the site ```shikimori.org```.
    2. and quotes.
#
**The website creates pictures without any temporary files**
#
# Quote example
[Quote](https://watashis.herokuapp.com/test)

![Quote](https://watashis.herokuapp.com/test)



# Api to get a quote
Send a post request to the link ``http://watashis.herokuapp.com/quotes`` data ```name``` (name quoted) ```text``` (text quote) ```date``` (year-month-day of the quote) ```ava``` (link to the avatar or photo quoted)

example for python3
using  library ```requests```
```pip3 install requests```
```python
import requests, io
from PIL import Image

data = {
    'name':'Nerv (anime Evangelion)',
    'text':'God’s in his Heaven… All’s right with the world',
    "date":'1995-10-04',
    "ava":'https://i.imgur.com/1xMbCHD.png'
    }
image = requests.post("https://watashis.herokuapp.com/quotes", data=data)
image = io.BytesIO(image.content)
a = Image.open(image)
a.show()
```

![Quote](https://i.imgur.com/JSpj7tD.png)
