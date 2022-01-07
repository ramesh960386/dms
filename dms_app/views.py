import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseForbidden, Http404
from django.http.response import FileResponse
from .models import DocumentModel
from django.conf import settings as se
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer


def responsedata(status, message, code, data={}):
    return {"success": status, "data": data, "code": code, "message": message}

def home(request):
    context = DocumentModel.objects.all()
    return render(request, "home.html", {'data': context})


class DocumentListView(generic.ListView):
    template_name = 'home.html'
    queryset = DocumentModel.objects.all()
    context_object_name = 'documents'
    # paginate_by = 10


class DocumentDetailView(generic.DetailView):
    model = DocumentModel
    template_name = 'detail.html'
    context_object_name = 'document'


def is_ajax(self):
    return self.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"


@api_view(['POST'])
@renderer_classes([JSONRenderer])
def file_mngt(request, id):
    print(request.headers)
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
    return HttpResponseForbidden('Not authorized to access this media.')


class DownloadFile(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request, id, format=None):
        try:
            obj = DocumentModel.objects.get(id=id)
            file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
            filename = os.path.basename(file_path)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                response['Content-Length'] = os.path.getsize(file_path)
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                return response
        except Exception as e:
            print(e)

class MediaAccess(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request, path):
        print(request.headers)
        try:
            obj = DocumentModel.objects.get(document='uploads/' + path)
            file_path = os.path.join(se.MEDIA_ROOT, obj.document.name)
            filename = os.path.basename(file_path)
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                response['Content-Length'] = os.path.getsize(file_path)
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                return response
        except Exception as e:
            print(e)


def media_access(request, path):
    print(request.headers)
    return HttpResponseForbidden('Not authorized to access this media.')