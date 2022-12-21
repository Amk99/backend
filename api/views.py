from rest_framework import generics,viewsets,status
from api import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post,Like,Comment

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


    def get(self, request, pk=None):
        # Get the post with the given pk
        post = get_object_or_404(Post, pk=pk)

        # Get all the comments for the post
        comments = post.comments.all()

        # Serialize the comments using the CommentSerializer
        serializer = serializers.CommentSerializer(comments, many=True)

        # Add the post id and post title to the response data
        data = {
            'post_id': post.id,
            'post_title': post.title,
            'post_description':post.description,
            'created_at':post.created_at,
            'comments': serializer.data,
            'likes':post.likes_count(),
        }

        # Return the serialized comments data in the response
        return Response(data)

    def delete(self, request, pk):
        post=Post.objects.get(pk=pk)
        if request.user != post.creator:
            return Response(
                {'message': "you do not have permission to do this action"},
                status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response({'message': 'post was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)




class LikeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        # Check if the user has already liked the post
        post = get_object_or_404(Post, id=pk)
        like = Like.objects.filter(user=request.user, post=post).first()
        if like is None:
            # Like the post if the user has not already liked it
            like = Like.objects.create(user=request.user, post=post)
            serializer = self.get_serializer(like)
            return Response(serializer.data)
        else:
            # Return an error if the user has already liked the post
            return Response({"error": "You have already liked this post."}, status=400)

    @action(detail=True, methods=['delete'])
    def unlike(self, request, pk=None):
        post = get_object_or_404(Post, id=pk)
        # Check if the user has liked the post
        like = Like.objects.filter(user=request.user, post=post).first()
        if like is not None:
            # Unlike the post if the user has liked it
            like.delete()
            return Response({"message":"Post Unliked"},status = 204)
        else:
            # Return an error if the user has not liked the post
            return Response({"error":"You have not liked the post."},status=400)



class CommentCreateView(generics.CreateAPIView):
    serializer_class = serializers.CommentSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request,pk):
        user = request.user
        post = get_object_or_404(Post, pk=pk)
        text = request.data.get('text')
        Comment.objects.create(author=user, post=post, text=text)
        return Response({"Message":f"You have commented {text} the post id {pk}."},status=400)



