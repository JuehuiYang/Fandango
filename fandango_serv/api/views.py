from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse
import json

# Create your views here.
from api.forms import FileUploadForm
from api.serv import handle_uploaded_file, setkeyword


def index(request):
    return HttpResponse("Hello, world. You're at the fandango serv index.")


# 设置关键词
@csrf_exempt
@require_http_methods(["POST"])
def upload_keyword(request):
    postBody = request.body
    json_result = json.loads(postBody)
    keyword = json_result['keyword']
    setkeyword(keyword)
    return JsonResponse(json_result)


# 接收上传的PDF文件
@csrf_exempt
@require_http_methods(["POST"])
def upload_file(request):
    error_msg = ""
    forms = FileUploadForm(request.POST, request.FILES)

    if forms.is_valid():
        handle_uploaded_file(request.FILES['file'])
        f = request.FILES['file']
        filename = request.FILES['file'].name
        print(filename)

    response = {
        'score': "ok",
    }
    return JsonResponse(response)


# 返回该pdf的评分及所有关键词出现的次数
@require_http_methods(["GET"])
def get_rating(request):

    data = {
        'name': 'xxx.pdf',
        'score': 5,
    }
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
