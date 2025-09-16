from dataclasses import fields
from rest_framework import serializers
from .models import Category, Tag, Task, TaskFile, User
from  rest_framework.validators import UniqueValidator

#
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

#Task Serializers
class TaskSerializer(serializers.ModelSerializer):
    # owner = serializers.StringRelatedField()
    # category = serializers.StringRelatedField()    
    class Meta:
        model = Task
        fields = '__all__'

#Tag Serializers        
class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = '__all__'

#Catogery Serializers        
class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = '__all__'

#TaskFile Serializers        
class TaskFileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TaskFile
        fields = '__all__'
        
