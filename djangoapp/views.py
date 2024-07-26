from django.db.migrations import serializer
from rest_framework import permissions, generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import *
from .serializers import ContentSerializer, RegisterSerializer, MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        refresh = serializer.refresh_token
        access = serializer.access_token

        response = Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key='access_token',
            value=access,
            httponly=True,
            secure=True,
            samesite='None'
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='None'
        )

        return response
# CRUD Views for Content
@api_view(['GET'])
def getContents(request):
    contents = Content.objects.all()
    serializer = ContentSerializer(contents, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getContent(request, pk):
    content = Content.objects.get(id=pk)
    serializer = ContentSerializer(content, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def addContent(request):
    # Check if content with the same title already exists
    if Content.objects.filter(title=request.data.get('title')).exists():
        return Response({'error': 'Content already exists with this title'}, status=status.HTTP_400_BAD_REQUEST)

    # Proceed with serialization and saving
    serializer = ContentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def updateContent(request, pk):
    content = Content.objects.get(id=pk)
    serializer = ContentSerializer(content, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def deleteContent(request, pk):
    content = Content.objects.get(id=pk)
    content.delete()
    return Response('Content successfully deleted!')


@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/register/',
        '/api/token/',
        '/api/token/refresh/',
        '/api/contents/',
        '/api/contents/<int:pk>/',

    ]
    return Response(routes)


