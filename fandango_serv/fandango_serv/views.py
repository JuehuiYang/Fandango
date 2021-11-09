from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the fandango serv index.")


# 接收上传的PDF文件及关键词
@require_http_methods(["GET"])
def upload_file(request):
    response = {}
    response['id'] = 111
    response['content'] = "This is what was identified.{}".format(111)
    return JsonResponse(response)


# 接收上传的PDF文件及关键词
@require_http_methods(["POST"])
def upload_keyword(request):
    response = {}
    return JsonResponse(response)


# 返回该pdf的评分及所有关键词出现的次数
def get_rating_(request):
    return JsonResponse("Hello, world. You\'re at the vote {} index.".format(id))


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
