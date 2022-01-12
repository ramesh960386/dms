from django.urls import path
from dms_app import views
from rest_framework.authtoken import views as token_views


urlpatterns = [
    # path('home/', views.home),
    path("", views.index, name="index"),
    path('documents/<int:pk>/', views.DocumentListView.as_view(), name='home'),
    path('detail/<int:pk>/', views.DocumentDetailView.as_view(), name='detail'),
    ################## api path #########################################
    path('api-token-auth/', token_views.obtain_auth_token, name='api-token-auth'),
    ################## api path #########################################
    path('media/uploads/<str:file>', views.MediaControl.as_view(), name="media"),
    path("aws", views.aws, name="aws")
]

# http POST http://localhost:8081/api-token-auth/ username='your_username' password="your_password"
