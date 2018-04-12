import os.path
import StringIO
import zipfile
import xlrd
import unicodecsv as csv

from django import forms

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives

from django.template import RequestContext
from django.http import  HttpResponse

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User

import dg.settings
from dg.settings import PERMISSION_DENIED_URL

import person
from data_upload.models import Document
from data_upload.forms import DocumentForm
from geographies.models import  Block
from coco.models import CocoUser


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='cocoadmin').count() > 0,
                  login_url=PERMISSION_DENIED_URL)
@csrf_protect
def home(request):
    """Home Page of static data upload"""
    form = DocumentForm(request.POST, request.FILES)
    user_id = User.objects.get(username=request.user.username).id
    blocks = CocoUser.objects.filter(user__id=user_id). \
             values_list('villages__block__block_name').distinct()
    block_names = [b for b in zip(*blocks)[0]]
    return render_to_response(
           'data_upload/netupload.html',
           {'form': form,
            'blocks': block_names},
            context_instance=RequestContext(request)
           )


# Handle file upload
def file_upload(request):
    """
    Upload data in the file to database.
    File formats: {.xls, .xlsx., .csv}
    """ 
    ext_allwd = ['.xls', '.xlsx']
    
    del person.ERROR_FILENAMES[:] #empty the list of files
    del person.SUCCESS_FILENAMES[:]
    
    user_id = User.objects.get(username=request.user.username).id
    block_id = Block.objects.get(block_name=request.POST.get("get_block")).id
    
    form = DocumentForm(request.POST, request.FILES)
    
    if not form.is_valid():
        raise forms.ValidationError("Invalid form")        

    document_raw = Document(docfile = request.FILES['docfile'], user_id = request.user)
     
    file_ext = os.path.splitext(document_raw.docfile.name)[-1]  
    
    error_list = []
    
    if (file_ext in ext_allwd):
        try:
            document_raw.save()
            document = file_converter(document_raw)
        except Exception, err:
            error_list.append(err)
    
    elif (file_ext == '.csv'):
        try:
            document_raw.save()
            document = document_raw.docfile.name
        except Exception, err:
            error_list.append(err)
    else:
        error_list.append('Invalid file format!!')    
    
    if len(error_list) > 0:
        return render_to_response("data_upload/ValidationErrorDisplay.html",
                                  {'valid_errors': error_list },
                                  context_instance=RequestContext(request))
   
    upload_success = person.upload_data(document, user_id, block_id)
    
    if not upload_success:
        valid_errors = ["Some field missing or mismatch. Please " + \
              "read instructions or download sample file"]
        return render_to_response("data_upload/ValidationErrorDisplay.html",
                                  {'valid_errors' : valid_errors },
                                  context_instance=RequestContext(request))
    
    send_mail(request)
    
    if(person.ERROR > 0):
        csv_data = csv_read()
        return render_to_response("data_upload/error.html", 
                                  {'csv_data' : csv_data},
                                  context_instance=RequestContext(request))
    else:
        return render_to_response("data_upload/success.html",
                                  context_instance=RequestContext(request))
    
  
def file_converter(document):
# converts file in .xls/.xlsx to .csv

    document_docfile_name = os.path.join(dg.settings.MEDIA_ROOT,
                                         document.docfile.name)
    wb = xlrd.open_workbook(document_docfile_name)
    worksheets = wb.sheet_names()
    
    # first sheet only
    sh = wb.sheet_by_name(worksheets[0])
    
    converted_csv_file = open(os.path.splitext(document_docfile_name)[0]+ \
                             '.csv', 'wb')
    wr = csv.writer(converted_csv_file, quoting=csv.QUOTE_ALL)
    #quote to none if char escape error pops up
    
    for rownum in xrange(sh.nrows):
        temp_list = [unicode(x).replace(u'\xa0', u'') for x in sh.row_values(rownum)]
        wr.writerow(temp_list)

        
    converted_csv_file.close()
    os.remove(document_docfile_name) #delete the old document
    
    return os.path.splitext(document_docfile_name)[0] +'.csv'
        
def handle_zip_download(request):
    
    buffer= StringIO.StringIO()
    zip_subdir = "error_files"
    zip_filename = "%s.zip" % zip_subdir
    
    zip_file= zipfile.ZipFile(buffer, "w")
    
    for f in (person.SUCCESS_FILENAMES + person.ERROR_FILENAMES):
        file = os.path.join(dg.settings.MEDIA_ROOT+r'/documents/', f)
        zip_path = os.path.join(str(zip_subdir), str(file)).split('/')[-1]
        zip_file.write(file, zip_path) #Add files to zip        
        
    zip_file.close() 
     
    resp = HttpResponse(buffer.getvalue(), 
                        content_type = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp
    

def csv_read():
    #display successfully upload data in success.html file    
    csv_data = []
    for file in person.SUCCESS_FILENAMES:
        file_data = []
        
        file = os.path.join(dg.settings.MEDIA_ROOT+r'/documents/', file)        
        
        csv_reader = csv.reader(open(file))
        csv_reader.next()
        for row in csv_reader:
            for column in row[1::2]:
                file_data.append(column)
        
        csv_data.append(file_data)
    
    return csv_data  
    

def send_mail(request):
    document = Document(docfile=request.FILES['docfile'])
    subject = "Status of uploaded file: "+document.docfile.name
    from_email = dg.settings.EMAIL_HOST_USER
    to_email = [request.POST.get("email_id")]
    
    if person.ERROR < 1:
        body = "All the data in uploaded file has been successfully entered"
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
    else:
        body = "Some of the data in uploaded file could not be entered." + \
               "Please find the attachment containing the error files "

        msg = EmailMultiAlternatives(subject, body, from_email, to_email)        
        for file in (person.ERROR_FILENAMES + person.SUCCESS_FILENAMES):
            file = os.path.join(dg.settings.MEDIA_ROOT+r'/documents/', file)
            msg.attach_file(file, 'text/csv' )            
    msg.send()
