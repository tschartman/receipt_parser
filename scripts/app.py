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
receiptArr = pytesseract.image_to_string(Image.open('test3.jpg'))
#find the index of the amount of items (should be direclty after the word SOLD)
index = receiptArr.split(' ').index("SOLD") + 1
coupons = len(re.findall(r"COUPON", receiptArr))
#try to parse the amount of items as an int
#coupons are shown directly under so include them 
items = int(re.findall(r"[0-9]*", receiptArr.split(' ')[index])[0]) + coupons


barcodeArr = re.findall(r"[0-9]{12}", receiptArr)    
for i in range(0, items):
    url = 'https://www.walmart.com/search/?query=' + barcodeArr[i]
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    data = json.loads(soup.find(id='searchContent').string)

    try:
        title = BeautifulSoup(data['searchContent']['preso']['items'][0]['title'], "html.parser").get_text()
        print(title)
    except IndexError:
        print("not found")
