import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from .forms import UploadFileForm
from .models import UploadFile


def upload_file(request):
    data = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            uf = UploadFile()
            uf.title = title
            uf.file = file
            uf.save()
            return HttpResponse("success!")
        else:
            # data['status'] = 'error'
            return HttpResponse("error!")
    else:
        form = UploadFileForm()
    return render(request, 'soft/upload.html', {
        'form': form,
        'file_list': UploadFile.objects.all(),
    })


def getfilename(title):
    return os.path.splitext(title)[0]


class uploadView(View):

    def get(self, request):
        form = UploadFileForm()
        file_list = UploadFile.objects.all()
        return render(request, 'soft/upload.html', {
            'form': form,
            'file_list': file_list,
        })

    def post(self, request):
        data = {}
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            file = form.cleaned_data['file']
            uf = UploadFile()
            if title.strip() == '':
                uf.title = getfilename(request.FILES['file'].name)
            else:
                uf.title = title
            uf.file = file
            size = round(request.FILES['file'].size/1024, 2)
            if size > 1024:
                uf.size = str(round(size/1024, 2)) + 'MB'
            else:
                uf.size = str(round(size, 1)) + 'KB'
            uf.save()
            data['status'] = 'success'
        else:
            data['status'] = 'error'
        return JsonResponse(data)


from django.views.generic.edit import FormView
from .forms import FileFieldForm


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'soft/upload.html'  # Replace with your template.
    success_url = '...'  # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        print(form)
        print(files)
        if form.is_valid():
            for f in files:
                ...  # Do something with each file.
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
