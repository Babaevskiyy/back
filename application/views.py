from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, serializers

from .models import *
from .serializers import *

@api_view(['POST'])
def StudentApplicationView(request):
    serializer = StudentApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def StudentApplication_ListView(request):
    application = StudentApplicationModel.objects.all()
    serializer = StudentApplicationSerializer(application,many=True)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def ManageApplicationView(request, pk):
    try:
        application = StudentApplicationModel.objects.get(pk=pk)
    except StudentApplicationModel.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = StudentApplicationSerializer(instance=application, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def NotificationApplicationView(request):
    serializer = NotificationApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def NotificationApplication_ListView(request):
    appliaction_notification = NotificationApplicationModel.objects.all()
    serializer = NotificationApplicationSerializer(appliaction_notification,many=True)
    return Response(serializer.data)