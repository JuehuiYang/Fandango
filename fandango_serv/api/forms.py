from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField(label="文件上传")
