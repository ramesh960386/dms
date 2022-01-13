import os
from django.http.response import FileResponse
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseForbidden, Http404
from django.conf import settings as se
from .models import DocumentModel
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        """
        This endpoints returns permission exempt
        it means any one can access this resource without login 
        """
        return request.method in SAFE_METHODS


@api_view(['GET'])
@permission_classes([IsAuthenticated | ReadOnly])
def hello_world(request):
    """any one can access this resource without login"""
    return Response({"message": "Hello, world!"})


def responsedata(status, message, code, data={}):
    return {"success": status, "data": data, "code": code, "message": message}


class MediaControl(APIView):
    # renderer_classes = [JSONRenderer]
    # permission_classes = (IsAuthenticated,)

    def get_object(self, **kwargs):
        try:
            return DocumentModel.objects.get(**kwargs)
        except DocumentModel.DoesNotExist:
            raise Http404

    def file_mngmt(self, file, option):
        try:
            obj = self.get_object(document="uploads/" + file)
            file_path = os.path.join(
                se.MEDIA_ROOT, obj.document.name).replace('\\', '/')
            filename = os.path.basename(file_path)

            if os.path.exists(file_path):
                response = FileResponse(
                    obj.document, content_type='application/pdf')
                # response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
                response['Content-Length'] = os.path.getsize(file_path)
                # response['Content-Disposition'] = "inline; filename=%s" % filename
                # response['Content-Disposition'] = "attachment; filename=%s" % filename
                response['Content-Disposition'] = "{}; filename={}".format(
                    option, filename)
                return response
            return Response({"data": "path doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)

    def get_file_access(self, request):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                # If admin, everything is granted
                return True
            else:
                # For simple user, only their documents can be accessed
                # doc = user.related_PRF_user.i_image  #Customize this...
                return True
        # return Response({'data': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
        # return HttpResponseForbidden('Not authorized to access this media.')
        return False

    def get(self, request, file):
        access_type = request.query_params.get('type')
        if self.get_file_access(request):
            return self.file_mngmt(file, access_type)
        return Response({'data': 'not allowed to access to this media file.'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, file):
        access_type = request.query_params.get('type')
        if self.get_file_access(request):
            print('ok')
            return self.file_mngmt(file, access_type)
        return Response({'data': 'not allowed to access to this media file.'}, status=status.HTTP_401_UNAUTHORIZED)


class MediaAccess(APIView):
    # permission_classes = [IsAuthenticated|ReadOnly]

    def get_object(self, **kwargs):
        try:
            return DocumentModel.objects.get(**kwargs)
        except DocumentModel.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        print('post method done')
        try:
            obj = self.get_object(pk=pk)
            file_path = os.path.join(
                se.MEDIA_ROOT, obj.document.name).replace('\\', '/')
            filename = os.path.basename(file_path)

            if os.path.exists(file_path):
                response = FileResponse(
                    obj.document, content_type='application/pdf')
                response['Content-Length'] = os.path.getsize(file_path)
                response['Content-Disposition'] = "attachment; filename=%s" % filename
                return response
            return Response({"data": "path doesn't exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'data': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
