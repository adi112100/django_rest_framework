from rest_framework import serializers
from restapi.models import Blog, Users, Blog_foruser

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog
		fields ='__all__'

class BlogForUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Blog_foruser
		fields ='__all__'

class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users
		fields = '__all__'

