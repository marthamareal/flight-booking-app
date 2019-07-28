from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer


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


class SingleUserView(generics.RetrieveUpdateDestroyAPIView):
    """ Generic view for retrieving, updating and deleting a user """
    # permission_classes = (IsAuthenticated,)
    queryset = User.objects.filter().all()
    serializer_class = UserSerializer
    model_name = 'User'