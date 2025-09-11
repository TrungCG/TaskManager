from ast import Delete
from calendar import c
from functools import partial
from django.shortcuts import render
from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from django.http import Http404

from .models import User,Task
from .serializers import SignupSerializer,TaskSerializer

class SignupView(APIView):
    def post(self, request):
        data = SignupSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                task = Task.objects.get(pk=pk)
            except Task.DoesNotExist:
                raise Http404("Task not found")
            data = TaskSerializer(task)
            return Response(data.data, status=status.HTTP_200_OK)
        else:
            tasks = Task.objects.all()
            data = TaskSerializer(tasks, many=True)
            return Response(data.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        task = TaskSerializer(data=request.data)
        if task.is_valid():
            task.save()
            return Response(task.data, status=status.HTTP_201_CREATED)
        return Response(task.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        data = TaskSerializer(task, data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        data = TaskSerializer(task, data=request.data, partial=True)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_200_OK)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
            