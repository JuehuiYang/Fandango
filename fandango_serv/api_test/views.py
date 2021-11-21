from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .forms import UploadFileForm, FileUploadForm

# Imaginary function to handle an uploaded file.
from .serv import handle_uploaded_file


@csrf_exempt
def index(request):
    return HttpResponse("Hello, world. You're at the fandango serv index.")

@csrf_exempt
def file_upload(request):
    error_msg = ""
    if request.method == 'POST':
        forms = FileUploadForm(request.POST, request.FILES)
        if forms.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('上传成功')
        error_msg = "异常"
    else:
        forms = FileUploadForm()
    data = {
        'name': 'xxx.pdf',
        'score': 5,
    }
    return JsonResponse(data)
