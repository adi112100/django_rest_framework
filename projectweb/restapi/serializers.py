from rest_framework import serializers
from restapi.models import Blog, Users, Admin

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields ='__all__'

class BlogForUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields = ['author', 'title', 'body', 'time', 'email']


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = '__all__'


class AdminSerializer(serializers.ModelSerializer):
	class Meta:
		model = Admin
		fields = '__all__'

