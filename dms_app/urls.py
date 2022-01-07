from django.urls import path
from dms_app import views

urlpatterns = [
    # path('home/', views.home),
    path('documents/', views.DocumentListView.as_view(), name='home'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='detail'),
    path('file_access/<int:id>/', views.file_mngt),
    path('file_download/<int:id>/', views.file_mngt),
    path('download_file/<int:id>/', views.DownloadFile.as_view()),
    ##
    # path('media/uploads/<str:path>', views.MediaAccess.as_view(), name='media'),
    path('media/uploads/<str:path>/', views.media_access, name='media'),
]
