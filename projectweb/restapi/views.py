from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from restapi.serializers import BlogSerializer, UsersSerializer, BlogForUserSerializer, AdminSerializer
from restapi.models import Blog, Users, Admin

from password_generator import PasswordGenerator
from django.core.mail import send_mail

@api_view(['GET'])
def allapi(request):
    return Response('''path('admin/', admin.site.urls),
    path('', views.allapi, name="allapi"),
    path('viewblog/', views.viewblog, name="viewblog"),
    path('newblog/', views.newblog, name="newblog"),
    path('deleteblog/<int:id>/', views.deleteblog, name="deleteblog"),
    path('approveblog/<int:id>/', views.approveblog, name="approveblog"),
    path('createuser/', views.createuser, name= "createuser"),
    path('requestkey/<str:email>/',views.requestkey, name= "requestkey")''')


@api_view(['GET', 'POST'])
def viewblog(request,id):
    
    if request.method=='POST':
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            if len(Admin.objects.filter(hashid = serializer.data['hashid']))!=0:
                if id == 'all':
                    blogs = Blog.objects.all()
                    serializer = BlogSerializer(blogs , many=True)
                    return Response(serializer.data)
                else:
                    try:
                        id = int(id)
                        blogs = Blog.objects.filter(id = id)
                        serializer = BlogSerializer(blogs , many=True)
                        return Response(serializer.data)
                    except:
                        return Response("API request is invalid!!")

            else:
                return Response("Admin hashid is incorrect!!")

    if id == 'all':
        blogs = Blog.objects.filter(status ='1')
        serializer = BlogForUserSerializer(blogs , many=True)
        return Response(serializer.data)
    else:
        try:
            id = int(id)
            blogs = Blog.objects.filter(status ='1').filter(id = id)
            serializer = BlogForUserSerializer(blogs , many=True)
            return Response(serializer.data)
        except:
            return Response("API request is invalid!!")





@api_view(['POST'])
def newblog(request):
    serializer = BlogSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        email = serializer.data['email']
        author = serializer.data['author']
        title = serializer.data['title']
        key = serializer.data['key']
        body = serializer.data['body']
        user = Users.objects.filter(email= email)
        if len(user)==0:
            return Response("Oops Something went wrong!!")
        else:
            user = user[0]
            if key == user.key:
                newblog = Blog(email=email, author=author, title=title, key=key, body=body, college=user.college, branch=user.branch, fullname=user.fullname)
                newblog.save()
            else:
                return Response("Oops Your key is not valid!! Please generate new key")





        return Response("Succesfully Created Blog!!")

    return Response("Blog isn't valid!!")

#  this api is call to approve pending blog by giving id as a parameter
@api_view(['POST'])
def approveblog(request, id):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        if len(Admin.objects.filter(hashid = serializer.data['hashid']))!=0:
            blog=Blog.objects.filter(id=id)
            if len(blog)!=0:
                blog=blog[0]
                if blog.status=='0':
                    blog.status = '1'
                    blog.save()
                    return Response("Succesfully verified Blog!!")
                else:
                    return Response("No Blog with given id!!")
            else:
                return Response("hash id is invalid!!")
    else:
        return Response("Request is not valid!!")
        


#  this api is call to delete any blog by giving id as a parameter
@api_view(['POST'])
def deleteblog(request, id):
    serializer = AdminSerializer(data=request.data)
    if serializer.is_valid():
        if len(Admin.objects.filter(hashid = serializer.data['hashid']))!=0:
            blog=Blog.objects.filter(id=id)
            
            if len(blog)!=0:

                blog=blog[0]
                blog.delete()
                return Response(f"Succesfully deleted blog with id {id}")
            else:
                return Response(f"No blog exist with id {id}")
        else:
            return Response("hashid is invalid!!")
    else:
        return Response(f"Request isn't valid")
    

@api_view(['POST'])
def requestkey(request):
    
    serializer = UsersSerializer(data = request.data)
    if serializer.is_valid():
        email = serializer.data['email']
        user = Users.objects.filter(email=email)
        if len(user)==0:
            
            usermail = serializer.data['email']
            usercollege = serializer.data['college']
            userbranch = serializer.data['branch']
            userfullname = serializer.data['fullname']
            newuser = Users(email=usermail, college= usercollege, branch = userbranch, fullname = userfullname)
            newuser.save()

    
        user = Users.objects.filter(email=email)
        user = user[0]
        pwo = PasswordGenerator()
        pwo.minlen = 30
        pwo.maxlen = 40
        hashkey=pwo.generate()
        issend = send_mail(f"Welcome back {user.fullname} !!", f"{hashkey}      is your validation key, Don't share it with anyone!!", 'khushimorankar96@gmail.com', [f"{user.email}"])
        usercollege = serializer.data['college']
        userbranch = serializer.data['branch']
        user.key = hashkey
        user.college = usercollege
        user.branch = userbranch
        user.save()
        return Response("Key has been succesfully mailed, Please check your email !!")

    else:
         return Response("Sorry Something went wrong")


    

#     return Response("Verification key is send to your email please check!!")
    
# @api_view(['POST'])
# def createuser(request):
#     serializer = UsersSerializer(data = request.data)
#     if serializer.is_valid():
#         if len( Users.objects.filter(email=serializer.data['email']).all() ) !=0:
#             return Response("email already taken")
#         else:
#             usermail = serializer.data['email']
#             usercollege = serializer.data['college']
#             userbranch = serializer.data['branch']
#             userfullname = serializer.data['fullname']

#             pwo = PasswordGenerator()
#             pwo.minlen = 30
#             pwo.maxlen = 40
#             hashkey=pwo.generate()
#             issend = send_mail(f"Welcome {userfullname}", f"{hashkey}      is your validation key, Don't share it with anyone!!", 'khushimorankar96@gmail.com', [f"{usermail}"])
#             if issend!=1:
#                 return Response("email is invalid!!")
#             userhashkey = hashkey
#             user = Users(email=usermail, college= usercollege, branch = userbranch, fullname = userfullname, hashkey = userhashkey)
#             user.save() 


#     # email = request.POST['email'] 
    
#     return Response("Hey!! your post is succesfully created once reviewed it will be live on our website!!")