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

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Simple image to string
receiptArr = pytesseract.image_to_string(Image.open('test2.jpg')).split('\n')

start = receiptArr.index('CAULIPOWER 086287100032 F 6.48 Y')

for index, line in enumerate(receiptArr):
        if(index >= start and index <= start + 3 ):  
            barcode = re.findall(r"[0-9]{12}", line)[0]     
            url = 'https://www.walmart.com/search/?query=' + barcode
            response = requests.get(url)

            soup = BeautifulSoup(response.text, "html.parser")

            data = json.loads(soup.find(id='searchContent').string)

            try:
                title = BeautifulSoup(data['searchContent']['preso']['items'][0]['title'], "html.parser").get_text()
                description = BeautifulSoup(data['searchContent']['preso']['items'][0]['description'], "html.parser").get_text()
                print("Title: ", title)
                print("Description: ", description)
                print('\n')
            except IndexError:
                print("not found")
