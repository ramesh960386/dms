from django.urls import path
from rest_framework.authtoken import views as token_views
from dms_app import views, api
from django.views.generic import TemplateView


urlpatterns = [
    path("", views.index, name="index"),
    path('documents/<int:pk>/', views.DocumentListView.as_view(), name='home'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='detail'),
    path("aws", views.aws, name="aws"),

    # api starts here
    path("hello_world/", api.hello_world, name="hello_world"),
    path('api-token-auth/', token_views.obtain_auth_token, name='api-token-auth'),
    path('media/uploads/<str:file>', api.MediaControl.as_view()),
    path('media_access/<int:pk>/', api.MediaAccess.as_view()),
    # api ends here
]
