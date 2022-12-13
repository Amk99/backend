from rest_framework import generics,viewsets,status
from api import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post

from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


User = get_user_model()

class UserList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

class UserDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class AuthClass(APIView):
    http_method_names = ['post']
    permission_classes = (AllowAny,)
    def post(self, request,format = None):
        email = request.data.get("email")
        password = request.data.get("password")
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=HTTP_400_BAD_REQUEST)
        user = authenticate(email=email, password=password)
        if not user:
            return Response({'error': 'Invalid Credentials'},
                            status=HTTP_404_NOT_FOUND)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key},
                        status=HTTP_200_OK)

class Logout(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response({'You have been logged out'},status=status.HTTP_200_OK)




class FollowView(viewsets.ViewSet):
    queryset = User.objects

    def follow(self, request, pk):
        # your follow code
        profile = User.objects.get(pk=pk)
        profile.followers.add(request.user)
        return Response({'message': 'now you are following'}, status=status.HTTP_200_OK)

    def unfollow(self, request, pk):
        profile = User.objects.get(pk=pk)
        profile.followers.remove(request.user)
        return Response({'message': 'you have unfollowed this user'}, status=status.HTTP_200_OK)


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    model = Post
    serializer_class = serializers.PostSerialzer
    def perform_create(self, serializer):
        serializer.save(creator_id=self.request.user.id)



class PostDetail(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerialzer
