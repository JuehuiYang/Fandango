import os


class Singleton(object):

    def foo(self):
        pass


singleton = Singleton()


def handle_uploaded_file(f):
    save_path = os.path.join(os.getcwd(), f.name)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)


# 处理计算关键词出现频率
def get_keywordcount():
    pass