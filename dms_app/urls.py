from django.urls import path
from rest_framework.authtoken import views as token_views
from dms_app import views, api
from django.views.generic import TemplateView

app_name = 'dms'

urlpatterns = [
    path("", views.index, name="index"),
    path('documents/<int:pk>/', views.DocumentListView.as_view(), name='myhome'),
    path('doc_add/<int:pk>/', views.DocumentAddFormView.as_view(), name='doc_add'),
    path('doc_update/<int:pk>/', views.DocumentUpdateView.as_view(), name='doc_edit'),
    path('doc_delete/<int:pk>/',
         views.DocumentDeleteView.as_view(), name='doc_delete'),

    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='detail'),

    # api starts here
    path("hello_world/", api.hello_world, name="hello_world"),
    path('api-token-auth/', token_views.obtain_auth_token, name='api-token-auth'),
    path('media/uploads/<str:file>', api.MediaControl.as_view()),
    path('media_access/<int:pk>/', api.MediaAccess.as_view()),
    # api ends here
    path("upload/<int:id>/", views.upload, name="upload"),
    path("delete/<int:id>/", views.delete, name="delete")
]
