from django import forms


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class FileUploadForm(forms.Form):
    file = forms.FileField(label="文件上传")
