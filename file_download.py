import os
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseForbidden, Http404
from django.http.response import FileResponse
from wsgiref.util import FileWrapper
from django.conf import settings as se
from dms_app.models import DocumentModel


def download_file1(request, id):
    obj = DocumentModel.objects.get(id=id)
    # file_path = obj.document.url[1:]
    file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
    filename = os.path.basename(file_path)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/pdf")
            response['Content-Length'] = os.path.getsize(file_path)  # obj.document.size
            response['Content-Disposition'] = "attachment; filename=%s" % filename
            return response
    raise Http404


def download_file2(request, id):
    obj = DocumentModel.objects.get(id=id)
    file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
    wrapper = FileWrapper(open(file_path, 'rb'))
    response = HttpResponse(wrapper, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(file_path)
    response['Content-Length'] = os.path.getsize(file_path)
    return response

def download_file3(request, id):
    obj = DocumentModel.objects.get(id=id)
    file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
    filename = os.path.basename(file_path)
    chunk_size = 8192
    response = StreamingHttpResponse(
       FileWrapper(open(file_path, 'rb'), chunk_size),
       content_type="application/octet-stream"
    )
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response

def show_pdf(request):
    filepath = os.path.join('media/uploads', 's_file.pdf')
    # https: // pythoncircle.com / post / 682 / how - to - display - pdf - in -browser - in -django - instead - of - downloading - it /
    # https: // www.csestack.org / render - open - pdf - file - django /
    # https: // pretagteam.com / question / how - to - display - pdfs - in -webpage - using - html - in -django
    return FileResponse(open(filepath, 'rb'), content_type='application/pdf')

def is_ajax(self):
    return self.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"

def media_access(request, path):
    file_path = DocumentModel.objects.filter(document='uploads/'+path)
    access_granted = False

    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            # If admin, everything is granted
            access_granted = True
        else:
            # For simple user, only their documents can be accessed
            # doc = user.related_PRF_user.i_image  #Customize this...
            access_granted = True

    if access_granted:
        open_path = file_path[0].document.url[1:]
        return FileResponse(open(open_path, 'rb'), content_type='application/pdf')
    else:
        return HttpResponseForbidden('Not authorized to access this media.')

# https://farhanghazi17.medium.com/django-react-link-to-download-pdf-a4c8da48802a
# super fine code
def file_mngt(request, id):
    obj = DocumentModel.objects.get(id=id)
    access_granted = False

    user = request.user
    if user.is_authenticated:
        if user.is_staff:
            # If admin, everything is granted
            access_granted = True
        else:
            # For simple user, only their documents can be accessed
            # doc = user.related_PRF_user.i_image  #Customize this...
            access_granted = True

    if access_granted:
        if is_ajax(request):
            try:
                file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
                filename = os.path.basename(file_path)
                if os.path.exists(file_path):
                    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                    response['Content-Length'] = os.path.getsize(file_path)
                    response['Content-Disposition'] = "attachment; filename=%s" % filename
                    return response
            except Exception as e:
                print(e)
        return HttpResponseForbidden('File is not allowed in browser.')
    return HttpResponseForbidden('Not authorized to access this media.')