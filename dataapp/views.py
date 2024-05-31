import pandas as pd
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
import tempfile

def handle_uploaded_file(f):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in f.chunks():
            tmp_file.write(chunk)
        file_path = tmp_file.name

    df = pd.read_excel(file_path)
    
    summary = df.groupby(['Cust State', 'DPD']).size().reset_index(name='Count')
    
    return summary

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            summary = handle_uploaded_file(request.FILES['file'])
            return render(request, 'dataapp/report.html', {'summary': summary.to_html(index=False)})
    else:
        form = UploadFileForm()
    return render(request, 'dataapp/upload.html', {'form': form})
