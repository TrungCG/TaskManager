from ast import Delete
from calendar import c
from functools import partial
from unicodedata import category
from django.shortcuts import render
from rest_framework.views import APIView
import rest_framework.status as status
from rest_framework.response import Response
from django.http import Http404

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
    def get(self, request, pk=None):
        if pk:
            try:
                serializer = Task.objects.get(pk=pk)
            except Task.DoesNotExist:
                raise Http404("Task not found")
            tasks = TaskSerializer(serializer)
            return Response(tasks.data, status=status.HTTP_200_OK)
        else:
            serializer = Task.objects.all()
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
    def post(self, request, pk):
        try: 
            serializer = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404("Task not found")        
        task_file = TaskFileSerializer(data = request.data)
        if task_file.is_valid():
            task_file.save(task=serializer)
            return Response(task_file.data, status= status.HTTP_201_CREATED)
        return Response(task_file.errors, status= status.HTTP_400_BAD_REQUEST)
    
    def put(self,request, pk):
        try:
            task_file = TaskFile.objects.get(pk=pk)
        except TaskFile.DoesNotExist:
            raise Http404("File not found")
        task_files = TaskFileSerializer(task_file, data=request.data)
        if task_files.is_valid():
            task_files.save()
            return Response(task_files.data, status=status.HTTP_200_OK)
        return Response(task_files.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            task_file = TaskFile.objects.get(pk=pk)
        except TaskFile.DoesNotExist:
            raise Http404("File not found")
        task_file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)