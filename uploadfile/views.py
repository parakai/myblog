from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy
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
            'file_order': UploadFile.objects.all().order_by('-download_nums')[:10],
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
                uf.title = f.name.split('/')[-1]
                uf.save()
            data['status'] = 'success'
            data['len'] = len(files)
        else:
            data['status'] = 'error'
        return JsonResponse(data)


from django.http import FileResponse
import os
from django.utils.http import urlquote


def file_download(request, file_path):
    ext = os.path.basename(file_path).split('.')[-1].lower()
    if ext not in ['py', 'db', 'sqlite3']:
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(os.path.basename(file_path)))
        return response
    else:
        raise Http404


class DownloadView2(View):
    def get(self, request, *args, **kwargs):
        dfile = get_object_or_404(UploadFile, pk=kwargs.get('file_pk'))
        name = dfile.file.name.split('/')[-1]
        response = FileResponse(open(dfile.file.path, 'rb'))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(urlquote(name))
        dfile.download_nums += 1
        dfile.save()
        return response


class DeleteSelectView(View):

    def get(self, request):
        return render(request, 'soft/delfile.html', {
            'file_lists': UploadFile.objects.all(),
        })

    def post(self, request):
        data = {}
        if not request.user.is_authenticated:
            data['status'] = 'fail'
            data['msg'] = "用户未登录"
            # 判断用户登录状态
            # return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
            return JsonResponse(data)
        pk_array = request.POST.getlist('ids[]')
        path_array = request.POST.getlist('filepaths[]')
        # print(path_array)
        utils.deletefile(path_array)
        idstring = ','.join(pk_array)
        # print(idstring)
        try:
            file_paths = UploadFile.objects.extra(where=['id in (' + idstring + ')']).select_for_update()
            UploadFile.objects.extra(where=['id in (' + idstring + ')']).delete()
            data['status'] = "success"
            data['msg'] = "操作成功！"
        except Exception:
            data['status'] = "fail"
            data['msg'] = "ID不存在！"
        return JsonResponse(data)


