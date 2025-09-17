import os
from ast import Delete
from calendar import c
from functools import partial
from unicodedata import category
from django.shortcuts import render
from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


from .models import User,Task, Category, Tag, TaskFile
from .serializers import SignupSerializer,TaskSerializer, CategorySerializer, TagSerializer
from .serializers import TaskFileSerializer
from API import serializers

#Signup
class SignupView(APIView):
    def post(self, request):
        user = SignupSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
        return Response(user.errors, status=status.HTTP_400_BAD_REQUEST)

#Task
class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk=None):
        if pk:
            try:
                serializer = Task.objects.get(pk=pk)
            except Task.DoesNotExist:
                raise Http404("Task not found")
            
            # kiểm tra quyền: chỉ owner hoặc admin mới được xem
            if serializer.owner != request.user and not request.user.is_staff:
                return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
            
            tasks = TaskSerializer(serializer)
            return Response(tasks.data, status=status.HTTP_200_OK)
        else:
            
            if request.user.is_staff:  # admin
                serializer = Task.objects.all()
            else:  # user thường
                serializer = Task.objects.filter(owner=request.user)
                
            # serializer = Task.objects.all()
            tasks = TaskSerializer(serializer, many=True)
            return Response(tasks.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        tasks = TaskSerializer(data=request.data)
        if tasks.is_valid():
            # tasks.save(owner=request.user)
            tasks.save()
            return Response(tasks.data, status=status.HTTP_201_CREATED)
        return Response(tasks.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            serializer = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        tasks = TaskSerializer(serializer, data=request.data)
        if tasks.is_valid():
            tasks.save()
            return Response(tasks.data, status=status.HTTP_200_OK)
        return Response(tasks.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            serializer = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        tasks = TaskSerializer(serializer, data=request.data, partial=True)
        if tasks.is_valid():
            tasks.save()
            return Response(tasks.data, status=status.HTTP_200_OK)
        return Response(tasks.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        try:
            tasks = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")
        tasks.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
#Category   
class CategoryView(APIView):
    def get(self, request, pk = None):
        if pk:
            try:
                serializer = Category.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404("Category not found")
            categorys = CategorySerializer(serializer)
            return Response(categorys.data, status= status.HTTP_200_OK)
        else:
            serializer = Category.objects.all()
            categorys = CategorySerializer(serializer, many=True)
            return Response(categorys.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        categorys = CategorySerializer(data=request.data)
        if categorys.is_valid():
            categorys.save()
            return Response(categorys.data, status=status.HTTP_201_CREATED)
        return Response(categorys.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            serializer = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Category not found")
        categorys = CategorySerializer(serializer, data = request.data)
        if categorys.is_valid():
            categorys.save()
            return Response(categorys.data, status=status.HTTP_200_OK)
        return Response(categorys.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def patch(self, request, pk):
        try:
            serializer = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Category not found")
        categorys = CategorySerializer(serializer, data = request.data, partial=True)
        if categorys.is_valid():
            categorys.save()
            return Response(categorys.data, status=status.HTTP_200_OK)
        return Response(categorys.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    def delete(self, request, pk):
        try:
            categorys = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Category not found")
        categorys.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
#Tag
class TagView(APIView):
    def get(self, request, pk=None):
        if pk:
            try:
                serializer = Tag.objects.get(pk=pk)
            except Tag.DoesNotExist:
                raise Http404("Tag not found")
            tags = TagSerializer(serializer)
            return Response(tags.data, status=status.HTTP_200_OK)
        else:
            serializer = Tag.objects.all()
            tags = TagSerializer(serializer, many = True)
            return Response(tags.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        tags = TagSerializer(data = request.data)
        if tags.is_valid():
            tags.save()
            return Response(tags.data, status=status.HTTP_201_CREATED)
        return Response(tags.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        try:
            serializer = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        tags = TagSerializer(serializer, data = request.data)
        if tags.is_valid():
            tags.save()
            return Response(tags.data, status=status.HTTP_200_OK)
        return Response(tags.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            tags = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise Http404("Tag not found")
        tags.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    
#TaskFile
class TaskFileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")

        # chỉ owner hoặc admin mới được upload
        if task.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)  # gắn file vào task
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        # try:
        #     tasks = Task.objects.get(pk=pk)
        # except Task.DoesNotExist:
        #     raise Http404("File not found")
        # if tasks.task.owner != request.user and not request.user.is_staff:
        #     return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        # # Xóa file vật lý trong MEDIA_ROOT
        # file_path = tasks.file_path.path
        # if os.path.exists(file_path):
        #     os.remove(file_path)
        # # Xóa record trong DB
        # tasks.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)
        
        
        try:
            task_file = TaskFile.objects.get(pk=pk)
        except TaskFile.DoesNotExist:
            raise Http404("File not found")

        # chỉ owner hoặc admin mới được xóa
        if task_file.task.owner != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

        # Xóa file vật lý trong MEDIA_ROOT
        file_path = task_file.file_path.path
        if os.path.exists(file_path):
            os.remove(file_path)

        # Xóa record trong DB
        task_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)