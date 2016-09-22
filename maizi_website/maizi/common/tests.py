from django.test import TestCase
from PIL import Image
import pytesseract,os,sys

# Create your tests here.
print(os.getcwd())
image = Image.open('yzm2.jpg')
vcode = pytesseract.image_to_string(image)
print(vcode)