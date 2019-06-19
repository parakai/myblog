from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .forms import FileFieldForm
from .forms import UploadFileForm
from .models import UploadFile
from . import utils


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
                uf.title = utils.getfilename(request.FILES['file'].name)
            else:
                uf.title = title
            uf.file = file
            size = round(request.FILES['file'].size/1024, 2)
            uf.size = utils.getfilesize(size)
            uf.save()
            data['status'] = 'success'
        else:
            data['status'] = 'error'
        return JsonResponse(data)


class FileFieldView(FormView):
    form_class = FileFieldForm
    template_name = 'soft/upload.html'  # Replace with your template.
    success_url = 'uploads'  # Replace with your URL or reverse().

    def get(self, request, *args, **kwargs):
        file_list = UploadFile.objects.all()
        return render(request, 'soft/upload.html', {
            'file_list': file_list,
            'form': FileFieldForm,
        })

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('file_field')
        data = {}
        if form.is_valid():
            for f in files:
                uf = UploadFile()
                uf.file = f
                uf.title = utils.getfilename(f.name)
                size = round(f.size / 1024, 2)
                uf.size = utils.getfilesize(size)
                uf.save()
            data['status'] = 'success'
        else:
            data['status'] = 'error'
        return JsonResponse(data)


class DelFileView(ListView):
    model = UploadFile
    template_name = 'soft/delfile.html'
    context_object_name = 'file_lists'
