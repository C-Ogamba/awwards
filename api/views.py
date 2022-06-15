from rest_framework.response import Response
from rest_framework.decorators import api_view
from award.models import Profile, Post
from .serializers import ProfileSerializer, PostSerializer

@api_view(['GET'])
def getData(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def addPost(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
def getData(request):
    profile = Profile.objects.all()
    serializer = ProfileSerializer(profile, many=True)
    
    return Response(serializer.data)

@api_view(['POST'])
def addProfile(request):
    serializer = ProfileSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)