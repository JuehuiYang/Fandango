from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
import json

# Create your views here.
from typing import List

from api.forms import FileUploadForm
from api.serv import handle_uploaded_file, set_keyword, get_zip, get_key_count_items


def index(request):
    return HttpResponse("Hello, world. You're at the fandango serv index.")


# 设置关键词
@csrf_exempt
@require_http_methods(["POST"])
def upload_keyword(request):
    print("wwwwww")
    print(request)
    print(request.POST.get('keyword'))
    keyword: str = request.POST.get('keyword')
    keys = json.loads(keyword)
    # keyword = json_result['keyword']
    set_keyword(keys)
    response = {
        'status': "ok",
    }
    return JsonResponse(response, safe=False)


# 获取词频
@csrf_exempt
@require_http_methods(["POST"])
def get_frequency(request):
    keyword: List[str] = json.loads(request.POST.get('keyword'))
    set_keyword(keyword)
    items = get_key_count_items(keyword)

    print(items)
    response = {
        'status': "ok",
        'items': items,
    }
    return JsonResponse(response, safe=False)


# 接收上传的PDF文件
@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    forms = FileUploadForm(request.POST, request.FILES)

    if forms.is_valid():
        handle_uploaded_file(request.FILES['file'])
        f = request.FILES['file']
        filename = request.FILES['file'].name
        print(filename)
    response = {
        'status': "ok",
    }
    return JsonResponse(response)


# 下载分析后的文件
@csrf_exempt
@require_http_methods(["GET"])
def download(request):
    the_file_name = 'result.zip'
    the_file_path = get_zip(the_file_name)
    zip_file = open(the_file_path, 'rb')
    return_response = HttpResponse(zip_file, content_type='application/force-download')
    return_response['Content-Disposition'] = 'attachment; filename="%s"' % the_file_name
    return_response['Content-Description'] = 'File Transfer'
    return_response['Content-Transfer-Enconding'] = 'binary'
    return return_response


# 返回该pdf的评分及所有关键词出现的次数
@require_http_methods(["GET"])
def get_rate(request):
    data = [
        {
            'key': 'hello',
            'count': 5,
        },
        {
            'key': 'world',
            'count': 10,
        },
    ]
    return JsonResponse(data)


# 下载原pdf文件
def get_source_file(request):
    return JsonResponse("Hello, world. You\'re at the vote {} index.".format(id))


# 下载标记后的pdf文件
def get_marked_file(request):
    return JsonResponse("Hello, world. You\'re at the vote {} index.".format(id))


# 获取设别出的文本内容
@require_http_methods(["GET"])
def get_text(request, id):
    response = {}
    try:
        response['id'] = id
        response['content'] = "This is what was identified.{}".format(id)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)
