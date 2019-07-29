try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import requests
import urllib.request
import time
import json
import re
from bs4 import BeautifulSoup

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Simple image to string
receiptArr = pytesseract.image_to_string(Image.open('test2.jpg'))

barcode = re.findall(r"[0-9]{12}", receiptArr)    
print(barcode)
for code in barcode:
    url = 'https://www.walmart.com/search/?query=' + code
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    data = json.loads(soup.find(id='searchContent').string)

    try:
        title = BeautifulSoup(data['searchContent']['preso']['items'][0]['title'], "html.parser").get_text()
        print(title)
    except IndexError:
        print("not found")
