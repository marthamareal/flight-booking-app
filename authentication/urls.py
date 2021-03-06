from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserView.as_view(), name='create_and_list_users'),
    path('users/login/', views.UserLoginView.as_view(), name='login'),
    path('users/<pk>/', views.SingleUserView.as_view(), name='single_user'),
    path('users/passport/upload/', views.UploadUserImage.as_view(), name='upload_photo'),

    ]

