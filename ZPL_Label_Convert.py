import os
import requests
import shutil
import base64  
import img2pdf
from PIL import Image
from zeep.exceptions import Fault
import urllib.request

def convert_zpl(ups_label):

    zpl = ups_label
    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
    files = {'file': zpl}
    headers = {'Accept': 'application/pdf', 'X-Rotation': '180'}  # omit this line to get PNG images back
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('Label/UPS.pdf', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
        out_file.close()

        if not out_file.closed:
            out_file.close()

        os.startfile('Label\\UPS.pdf', 'print')
    else:
        print('Error-ZPL: ' + response.text)


def convert_zpl_RSL(ups_label):

    zpl = ups_label
    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
    files = {'file': zpl}
    headers = {'Accept': 'application/pdf', 'X-Rotation': '180'}  # omit this line to get PNG images back  ,
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('Label/UPS_RSL.pdf', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
        out_file.close()

        if not out_file.closed:
            out_file.close()

        os.startfile('Label\\UPS_RSL.pdf', 'print')
    else:
        print('Error-ZPL RSL: ' + response.text)

def convert_zpl_Reprint(ups_label):

    zpl = ups_label

    # adjust print density (8dpmm), label width (4 inches), label height (6 inches), and label index (0) as necessary
    url = 'http://api.labelary.com/v1/printers/8dpmm/labels/4x6/0/'
    files = {'file': zpl}
    headers = {'Accept': 'application/pdf', 'X-Rotation': '180'}  # omit this line to get PNG images back  ,
    response = requests.post(url, headers=headers, files=files, stream=True)

    if response.status_code == 200:
        response.raw.decode_content = True
        with open('Label/UPS_RePrintLabel.pdf', 'wb') as out_file:  # change file name for PNG images
            shutil.copyfileobj(response.raw, out_file)
        out_file.close()

        if not out_file.closed:
            out_file.close()

        os.startfile('Label\\UPS_RePrintLabel.pdf', 'print')
    else:
        print('Error-ZPL REPRINT: ' + response.text)


def USPS_convert_zpl(url):
    try:
        response = urllib.request.urlopen(url)

        with open('Label/usps.pdf', 'wb') as fh:
            fh.write(response.read())
        fh.close()

        if not fh.closed:
            fh.close()

        os.startfile('Label\\usps.pdf', 'print')

    except Fault as e:
        print("ERROR-ZPL USPS" + str(e))

def USPS_RSL_convert_zpl(url):
    try:
        response = urllib.request.urlopen(url)

        # with open("Image/usps_rsl.png", "wb") as fh:
        #     fh.write(base64.decodebytes(response))
        #
        # image = Image.open('Image/usps_rsl.png')
        # pdf_label = img2pdf.convert(image.filename)

        with open('Label/usps_rsl.pdf', 'wb') as fh:
            fh.write(response.read())
        fh.close()

        if not fh.closed:
            fh.close()

        os.startfile('Label\\usps_rsl.pdf', 'print')

    except Fault as e:
        print("ERROR-ZPL USPS RSL" + str(e))

def USPS_international_convert_zpl(url):
    try:
        response = urllib.request.urlopen(url)

        with open('Label/international.pdf', 'wb') as fh:
            fh.write(response.read())
        fh.close()

        if not fh.closed:
            fh.close()

        os.startfile('Label\\international.pdf', 'print')

    except Fault as e:
        print("ERROR-ZPL International: " + str(e))


def printNoti(string):
    try:
        if string == 'UPS 2nd Day Air':
            os.startfile('Label\\2nd.docx', 'print')
        elif string == 'UPS Overnight':
            os.startfile('Label\\overnight.docx', 'print')

    except Fault as e:
        print("ERROR-ZPL Noti: " + str(e))