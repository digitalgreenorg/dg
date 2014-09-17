import  os.path, dg.settings, StringIO, zipfile

from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.core.mail import EmailMultiAlternatives
from django.core.management import setup_environ
setup_environ(dg.settings)

from django.template import RequestContext
from django.http import  HttpResponse

from django import forms
import xlrd, csv, person

from django.contrib.auth.decorators import login_required, user_passes_test
from dg.settings import PERMISSION_DENIED_URL
from django.contrib.auth.models import User

from data_upload.models import Document
from data_upload.forms import DocumentForm
from geographies.models import  Block
from coco.models import CocoUser

@login_required()
@user_passes_test(lambda u: u.groups.filter(name='cocoadmin').count() > 0, 
                  login_url=PERMISSION_DENIED_URL)
@csrf_protect

# home page
def home(request):
    form = DocumentForm(request.POST, request.FILES)
    user_id = User.objects.get(username=request.user.username).id
    blocks = CocoUser.objects.filter(user__id=user_id).values_list('villages__block__block_name').distinct() 
    
    block_names = [str(b) for b in zip(*blocks)[0]]
    
    return render_to_response(
           'data_upload/netupload.html',
           {'form' : form, 'blocks' : block_names},
            context_instance=RequestContext(request)
           )

# Handle file upload   
def file_upload(request): 
    ext_allwd = ['.xls', '.xlsx']
    
    del person.ERROR_FILENAMES[:] #empty the list of files
    del person.SUCCESS_FILENAMES[:]
    
    user_id = User.objects.get(username=request.user.username).id
    block_id = Block.objects.get(block_name=request.POST.get("get_block")).id
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            document = Document(docfile=request.FILES['docfile'])
             
            if (os.path.splitext(document.docfile.name)[1] in ext_allwd):
                document.save()
                converted_document = file_converter(document)
                status = person.add_person(converted_document, user_id,block_id)
                if status == 1:
                    raise forms.ValidationError("Some field missing or mismatch." \
                                                "Please read instructions or download sample file")
            
            elif (os.path.splitext(document.docfile.name)[1] == '.csv'):
                document.save()
                status=person.add_person(document.docfile.name, user_id, block_id)
                if status == 1:
                    raise forms.ValidationError("Some field missing or mismatch." \
                                                "Please read instructions or download sample file")
    else:
        form = DocumentForm()  # A empty, unbound form

    if (person.ERROR > 0):
            csv_data = csv_to_html()
            #send_mail(request)
            return render_to_response("data_upload/error.html", 
                                      {'csv_data' : csv_data},
                                      context_instance=RequestContext(request)
                                      )
    else:
            #send_mail(request)
            return render_to_response(
                                      'data_upload/success.html',
                                      context_instance=RequestContext(request)
                                      )
    

#converts .xls and .xlsx files to .csv    
def file_converter(document):
    try:
        document_docfile_name = os.path.join(dg.settings.MEDIA_ROOT,
                                             document.docfile.name)
        
        wb = xlrd.open_workbook(document_docfile_name)
        worksheets = wb.sheet_names()
        sh = wb.sheet_by_name(worksheets[0])
        
        converted_csv_file = open(os.path.splitext(document_docfile_name)[0] +'.csv', 'wb')
        wr = csv.writer(converted_csv_file, quoting=csv.QUOTE_NONE)
        
        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))
        converted_csv_file.close()    
        os.remove(document_docfile_name) #delete the old document
        return os.path.splitext(document_docfile_name)[0] +'.csv'

    except Exception, err:
        print err
        
        
def handle_zip_download(request):
    
    buffer= StringIO.StringIO()
    zip_subdir = "error_files"
    zip_filename = "%s.zip" % zip_subdir
    
    zip_file= zipfile.ZipFile( buffer, "w" )
    
    for f in person.ERROR_FILENAMES:
        file = os.path.join(dg.settings.MEDIA_ROOT+r'documents/', f)
        zip_path = os.path.join(str(zip_subdir), str(file)).split('/')[-1]
        zip_file.write(file, zip_path) #Add files to zip
        
    for f in person.SUCCESS_FILENAMES:
        file = os.path.join(dg.settings.MEDIA_ROOT+r'documents/', f)
        zip_path = os.path.join(str(zip_subdir), str(file)).split('/')[-1]
        zip_file.write(file, zip_path) #Add files to zip
        
        
    zip_file.close() 
       
     
    resp = HttpResponse(buffer.getvalue(), 
                        mimetype = "application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp
    
def csv_to_html():
    # enter success file datas from village, shg and person into each list in list of lists
    csv_data = [[] for i in range(3)]
    
    i = 0
    for file in person.SUCCESS_FILENAMES:
        if i < 3:
            file = os.path.join(dg.settings.MEDIA_ROOT+r'documents/', file)
            
            csv_reader = csv.reader(open(file))
            row_num = 0
            for x in csv_data:
                for row in csv_reader:
                    for column in row:
                        csv_data[i].append(column)
                       
            row_num += 1
            i +=1 
       
    return csv_data


def send_mail(request):
    document = Document(docfile=request.FILES['docfile'])
    subject = "Status of uploaded file: "+document.docfile.name
    from_email = dg.settings.EMAIL_HOST_USER
    to_email = [request.POST.get("email_id")]
    if person.ERROR < 1:
        body = "All the data in uploaded file has been successfully entered"
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        msg.send()
    else:
        body = "Some of the data in uploaded file could not be entered." \
               "Please find the attachment containing the error files "
        msg = EmailMultiAlternatives(subject, body, from_email, to_email)
        for file in person.ERROR_FILENAMES:
            file = os.path.join(dg.settings.MEDIA_ROOT+r'documents/', file)
            msg.attach_file(file, 'text/csv' )
            
        for file in person.SUCCESS_FILENAMES:
            file = os.path.join(dg.settings.MEDIA_ROOT+r'documents/', file)
            msg.attach_file(file, 'text/csv' )
        msg.send()
