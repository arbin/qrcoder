# Create your views here.
from django.template.response import TemplateResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.template import Template, Context

from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

import Image
import os
import uuid
import zipfile

from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

from cStringIO import StringIO

try:
    import qrcode
except ImportError:
    qrcode = None

try:
    import PyQRNative
except ImportError:
    PyQRNative = None

QR_DIR = settings.QR_DIR
QR_FILE_DIR = settings.QR_FILE_DIR
MERGE_FILE_DIR = settings.MERGE_FILE_DIR
FILE_UPLOAD_DIR = settings.FILE_UPLOAD_DIR
PDF_FILE = settings.PDF_FILE

def get_unique_filename():
    unique_filename = uuid.uuid4()
    unique_filename = str(unique_filename).split("-")
    unique_filename = unique_filename[0]
    return unique_filename

def count_qr():
    count = 0
    for qr in os.listdir(QR_DIR):
        if qr.endswith(".png"):
            count+=1
    return str(count)

def process_data(data, filename):

    """ QR version 1 """
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    x = qr.make_image()
    filename1 = "qrcode."+get_unique_filename()+".png"
    qr_file = os.path.join(QR_FILE_DIR, filename1)
    img_file = open(qr_file, 'wb')
    x.save(img_file, 'PNG')
    img_file.close()

    """ QR version 40 """
    qr = PyQRNative.QRCode(20, PyQRNative.QRErrorCorrectLevel.L)
    qr.addData(data)
    qr.make()
    im = qr.makeImage()
    filename2 = "qrcode."+get_unique_filename()+".40.png"
    qr_file = os.path.join(QR_FILE_DIR, filename2)
    img_file = open(qr_file, 'wb')
    im.save(img_file, 'PNG')
    img_file.close()

    """ Zip qr code files """
    zipfilename = "qrcoder."+get_unique_filename()+".zip"
    qrZipFile = zipfile.ZipFile(os.path.join(QR_FILE_DIR, ("zip/" + zipfilename)), "a" )
    qrZipFile.write(os.path.join(QR_FILE_DIR, filename1), filename1, zipfile.ZIP_DEFLATED )
    qrZipFile.write(os.path.join(QR_FILE_DIR, filename2), filename2, zipfile.ZIP_DEFLATED )
    qrZipFile.close()

    return filename1, filename2, zipfilename

def home(request):
    numqr = count_qr()
    if request.method == 'POST':
        for key, value in request.POST.iteritems():
            if key == "url":
                data = value
                name = "website.url"
            elif key == "twitter":
                data= "http://mobile.twitter.com/" + value
                name = "twitter"
            elif key == "skypename":
                data = '<a href="skype:'+ value + '?chat">'
                name = "skype"
            elif key == 'fbpage':
                data = "http://facebook.com/" + value
                name = "fbpage"
            elif key == "fburlpage":
                data = '<a href="http://facebook.com/' + request.POST['fburlpage'] + '>' + request.POST['fbtitle'] + '</a>'
                name = "fblike"
            elif key == "message":
                data = value
                name = "text"
            elif key == "vcard":
                data = "BEGIN:VCARD\nVERSION:4.0\nN:" + request.POST['lastname'] + ";" + request.POST['firstname'] + ";;;\n" + \
                    "FN:" + request.POST['firstname'] + request.POST['lastname'] + "\n" \
                    "ORG:" + request.POST['org'] + "\n" \
                    "TITLE:" + request.POST['jobtitle'] + "\n" \
                    "TEL;TYPE=cell,voice;VALUE=uri:tel:" + request.POST['celno'] + "\n" \
                    "TEL;TYPE=home,voice;VALUE=uri:tel:" + request.POST['telno'] + "\n" \
                    "ADR;TYPE=work;LABEL=" + request.POST['streetad'] + "\n" + request.POST['city'] + "," + request.POST['state'] + "\n" \
                    + request.POST['zip'] + request.POST['country'] + "\n" \
                    ":;;" + request.POST['streetad'] + ";" + request.POST['city'] + ";" + request.POST['state'] + ";" + request.POST['zip'] + ";" + request.POST['country'] + "\n" \
                    "EMAIL:" + request.POST['email'] + "\n" \
                    "URL:" + request.POST['website'] + "\nREV:20080424T195243Z\nEND:VCARD"
                name = "vcard"
            elif key == "telno":
                data = "VALUE=uri:tel:+" + value
                name = "telno"
            elif key == "email":
                data = "sendmail"
                name = "sendmail"

        if data != "sendmail":
            qrcode1, qrcode40, downloadzip = process_data(data, name)
            
            return render_to_response('home.html', dict(
                    qroutput1 = qrcode1,
                    qroutput40 = qrcode40,
                    download = downloadzip,
                    pdfprint = "",
                    totalqr = numqr,
                    qrmerge = "qroutput.merge.png"), context_instance=RequestContext(request))
        else:
            msg = sendmail(request)
            print msg
            return render_to_response('home.html', dict(
                qroutput1 = "qrcode.website.url.png",
                qroutput40 = "qrcode.website.url.40.png",
                download = "",
                pdfprint = "",
                totalqr = numqr,
                qrmerge = "qroutput.merge.png"), context_instance=RequestContext(request))

    else:
        return render_to_response('home.html', dict(
                qroutput1 = "qrcode.website.url.png",
                qroutput40 = "qrcode.website.url.40.png",
                download = "",
                pdfprint = "",
                totalqr = numqr,
                qrmerge = "qroutput.merge.png"), context_instance=RequestContext(request))

def merge_image(b_image, f_image, position):
    f_image = os.path.join(QR_FILE_DIR, f_image)
    foreground = Image.open(f_image)
    resized_qrcode = foreground.resize((100, 100), Image.ANTIALIAS)
    background = Image.open(b_image)
    resized_background = background.resize((400, 200), Image.ANTIALIAS)
    resized_background.save(b_image)
    background = Image.open(b_image)
    if position == 'center':
        background.paste(resized_qrcode, (150,50)) # center
    elif position == 'bottom-left':
        background.paste(resized_qrcode, (1,99)) # lower left
    elif position == 'bottom-right':
        background.paste(resized_qrcode, (299,99)) # lower right
    elif position == 'upper-left':
        background.paste(resized_qrcode, (1,1)) # upper left
    else:
        background.paste(resized_qrcode, (299,1)) # upper right

    image_filename = "image." + get_unique_filename() + ".output.png"
    background.save(MERGE_FILE_DIR + image_filename, "PNG")

    return image_filename

def uploads(request):
    b_filename = request.FILES['background'].name
    b_destination = open(FILE_UPLOAD_DIR + b_filename, 'wb+')
    for chunk in request.FILES['background'].chunks():
        b_destination.write(chunk)
    b_destination.close()

    version = request.POST['version']
    if version == "version1":
        f_filename = request.POST['qrcode1']
    elif version == "version40":
        f_filename = request.POST['qrcode40']
    position = request.POST['position']

    imagefilename = merge_image(FILE_UPLOAD_DIR + b_filename, f_filename, position)

    return render_to_response('home.html', dict(
                qroutput1 = request.POST['qrcode1'],
                qroutput40 = request.POST['qrcode40'],
                download = "",
                qrmerge = imagefilename), context_instance=RequestContext(request))

def about(request):
    return TemplateResponse(request, 'about.html', None)

def faqs(request):
    return TemplateResponse(request, 'faqs.html', None)

def how_it_works(request):
    return TemplateResponse(request, 'how-it-works.html', None)

def email(request):
    return TemplateResponse(request, 'email.html', None)

def prints(request):
    return TemplateResponse(request, 'print.html', None)

def custom(request):
    return TemplateResponse(request, 'custom.html', None)

def arbin(request):
    return TemplateResponse(request, 'arbin.html', None)

def print_qr(data):
    """ This will create PDF with QR images on a 2x2 inch size in an A4 paper. """
    filename = get_unique_filename()
    filename = "qrcoder." + filename + ".pdf"
    
    PDF_FILE = PDF_FILE + filename
    pdf = canvas.Canvas(PDF_FILE)

    qr_code = QrCodeWidget(data)
    b = qr_code.getBounds()

    width = b[2]-b[0]
    height = b[3]-b[1]

    # For 2x2 inch size layout on A4
    col1 = ['col1a', 'col1b', 'col1c', 'col1d']
    col2 = ['col2a', 'col2b', 'col2c', 'col2d']
    col3 = ['col3a', 'col3b', 'col3c', 'col3d']
    pos1 = ['1, 1', '0, 215', '0, 430', '0, 645']
    pos2 = ['205, 1', '205, 215', '205, 430', '205, 645']
    pos3 = ['405, 1', '405, 215', '405, 430', '405, 645']

    im_size = Drawing(200,200,transform = [200./width,0,0,200./height,0,0])

    for items in col1:
        items = im_size
        items.add(qr_code)
        for pos in pos1:
            renderPDF.draw(items, pdf, int(pos.split(",")[0]), int(pos.split(",")[1]))

    for items in col2:
        items = im_size
        items.add(qr_code)
        for pos in pos2:
            renderPDF.draw(items, pdf, int(pos.split(",")[0]), int(pos.split(",")[1]))

    for items in col3:
        items = im_size
        items.add(qr_code)
        for pos in pos3:
            renderPDF.draw(items, pdf, int(pos.split(",")[0]), int(pos.split(",")[1]))

    pdf.showPage()
    pdf.save()
    return filename

def sendmail(request):
    if request.method == 'POST':
        subject = 'QR Code'
        sender = 'QR Coder <qrcoder@pysoldev.com>'
        recipient = request.POST['email']
        qrzip = request.POST['qrzip']
        try:
            email = EmailMessage(subject, "Hi There! It's an email with a QR codes attached in it. ", sender, recipient)
            email.attach(qrzip.name, qrzip.read(), qrzip.content_type)
            email.send()

            messages.success(request, "<h1>Sending email..</h1> <p>Thanks "
                                      "for sharing. ")
            return "Message sent!"
        except:
            return "Error sending email."
