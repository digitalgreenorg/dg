import xlrd, csv
from django.contrib import messages
import os.path
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


from xl_import.models import Document
from xl_import.forms import DocumentForm

#root = tk.Tk()
#root.withdraw()
def list(request):
    ext_allwd = ['.xls', '.xlsx']
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])

            if (os.path.splitext(newdoc.docfile.name)[1] in ext_allwd):
                newdoc.save()
                file_converter(newdoc)
                #tkMessageBox.showinfo(title="xl_import", message="File uploaded successfully")
                
            elif (os.path.splitext(newdoc.docfile.name)[1] == '.csv'):
                newdoc.save()
                #tkMessageBox.showinfo(title="xl_import", message="File uploaded successfully")
                
            else:
                messages.add_message(request, messages.ERROR, 'Hello world.')
                #tkMessageBox.showerror(title="xl_import", message="Invalid file format!")
                
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('xl_import.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'xl_import/netupload.html',
       {'documents': documents, 'form': form},
        context_instance=RequestContext(request)
    )


def file_converter(newdoc):
    try:
        working_dir = r"C:\Users\abhi_1510\Documents\dg\dg\media\social_website\uploads"

        newdoc_docfile_name = os.path.join(working_dir, newdoc.docfile.name)

        print newdoc.docfile.name
        wb = xlrd.open_workbook(newdoc_docfile_name)

        sh = wb.sheet_by_name('Sheet1')
        your_csv_file = open(os.path.splitext(newdoc_docfile_name)[0] +'.csv', 'wb')

        wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)
        for rownum in xrange(sh.nrows):
            wr.writerow(sh.row_values(rownum))

        os.remove(newdoc_docfile_name)
        return your_csv_file

    except Exception, err:
        print err