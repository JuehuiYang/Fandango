from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

def save_file(file):
    with open('somefile.txt', 'wb') as fp:
        for chunk in file.chunks():
            fp.write(chunk)


class IndexView(View):
    # 如果是GET请求，直接渲染到上传文件页面
    def get(self, request):
        return render(request, 'one/index.html')

    # 如果是POST请求，那么将接收文件的值
    def post(self, request):
        # 获取前台传来的文件
        myfile = request.FILES.get('myfile')
        # 调用自定义的save_file()方法，将文件保存到服务器
        save_file(myfile)

        return HttpResponse("SUCCESS")

urlpatterns = [
    path('', IndexView.as_view()),
]
