from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

import mimetypes
import os

from .forms import DocumentForm
from .models import Document

from .process import process

def index(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # CORRECT PATH
            context = {'form': form}
            return redirect('/uploaded/', context)
    else:
        form = DocumentForm()  # An empty, unbound form
        context = {'form': form}
        return render(request, 'process/index.html', context)

def uploaded(request):
    file = Document.objects.latest('id').docfile
    
    process(file)

    return render(request, 'process/upload.html')


def download(request):
    # Define Django project base directory
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Define text file name
    file = Document.objects.latest('id').docfile
    filename = file.name
    filename = filename.split("/")[-1]
    filename = filename.rsplit(".", 1)[0] 
    filename += '.xlsx'
    # Define the full file path
    filepath = BASE_DIR + '\\' + filename
    # Open the file for reading content
    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response