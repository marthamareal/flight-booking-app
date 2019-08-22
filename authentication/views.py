from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import cloudinary.uploader

from authentication.models import User
from authentication.serializers import UserSerializer, LoginSerializer


class UserView(generics.ListCreateAPIView):
    """ Generic view for creating and listing all users """
    permission_classes = (AllowAny,)
    queryset = User.objects.filter().all()
    serializer_class = UserSerializer
    model_name = 'User'

    def post(self, request, *args, **kwargs):
        """ Method for creating an object"""

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            'message': 'Your account has been successfully created.you can login with your email and password.',
            'status': status.HTTP_201_CREATED
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    """ Generic view for loging in a user """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = {
            "id": serializer.data['id'],
            "email": serializer.data['email'],
            "token": serializer.data['token'],
            "message": "You have successfully logged in."
        }
        return Response(response, status=status.HTTP_200_OK)


class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view for retrieving, updating and deleting a user """
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter().all()
    serializer_class = UserSerializer
    model_name = 'User'


class UploadUserImage(APIView):
    parser_classes = MultiPartParser, JSONParser

    @staticmethod
    def put(request):
        queryset = User.objects.all()
        photo = request.data.get('passport_photo')
        if photo:
            user = get_object_or_404(queryset=queryset, pk=request.user.id)
            upload_data = cloudinary.uploader.upload(photo)

            user.image_url = upload_data.get('secure_url')
            user.save()

            return Response({
                'message': 'You have successfully uploaded your photo',
                'image_info': upload_data,
            }, status=status.HTTP_200_OK)
        return Response({
                'error': 'Please provide a passport_photo you want to upload'
            }, status=status.HTTP_400_BAD_REQUEST)
