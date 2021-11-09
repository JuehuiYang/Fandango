import os


def handle_uploaded_file(f):
    save_path = os.path.join(os.getcwd(), f.name)
    with open(save_path, 'wb+') as fp:
        for chunk in f.chunks():
            fp.write(chunk)

