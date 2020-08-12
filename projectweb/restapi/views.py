from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from restapi.serializers import BlogSerializer, UsersSerializer, BlogForUserSerializer
from restapi.models import Blog, Users, Blog_foruser

from password_generator import PasswordGenerator
from django.core.mail import send_mail

@api_view(['GET'])
def allapi(request):
    return Response('''path('admin/', admin.site.urls),
    path('', views.allapi, name="allapi"),
    path('viewblog/', views.viewblog, name="viewblog"),
    path('adminviewblog/', views.adminviewblog, name="adminviewblog"),
    path('newblog/', views.newblog, name="newblog"),
    path('deleteblog/<int:id>/', views.deleteblog, name="deleteblog"),
    path('approveblog/<int:id>/', views.approveblog, name="approveblog"),
    path('createuser/', views.createuser, name= "createuser"),
    path('requestkey/<str:email>/',views.requestkey, name= "requestkey")''')


@api_view(['GET'])
def viewblog(request):
    blogs = Blog_foruser.objects.all()
    serializer = BlogForUserSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def adminviewblog(request):
    blogs = Blog.objects.all()
    serializer = BlogSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def newblog(request):
    serializer = BlogSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        email = serializer.data['email']
        author = serializer.data['author']
        title = serializer.data['title']
        key = serializer.data['key']
        blog = serializer.data['blog']
        user = Users.objects.filter(email= email)
        if len(user)==0:
            return Response("Oops Your email is not registered!! Please register your email in our server")
        else:
            user = user[0]
            if key == user.hashkey:
                newblog = Blog(email=email, author=author, title=title, key=key, blog=blog)
                newblog.save()
            else:
                return Response("Oops Your key is not valid!! Please generate new key")





        return Response("Succesfully Created Blog!!")

    return Response("Blog isn't valid!!")

@api_view(['GET'])
def approveblog(request, id):
    blog=Blog.objects.filter(id=id)
    if len(blog)!=0:
        blog=blog[0]
        if blog.status=='pending':
            blog.status = 'verified'
            bloguser = Blog_foruser(author = blog.author, title = blog.title, blog = blog.blog, time = blog.time, status = 'verified')
            bloguser.save()
            blog.save()
            return Response("Succesfully verified Blog!!")
        else:
            return Response("No Blog with given id!!")
        



@api_view(['GET'])
def deleteblog(request, id):
    blog=Blog.objects.filter(id=id)
    
    if len(blog)!=0:
        blog=blog[0]
        bloguser = Blog_foruser.objects.filter(time = blog.time).filter(title = blog.title).filter(blog = blog.blog)
        if len(bloguser)!=0:
            bloguser.delete()
        blog.delete()
        return Response(f"Succesfully deleted blog with id {id}")
    return Response(f"No blog exist with id {id}")
    
@api_view(['POST'])
def createuser(request):
    serializer = UsersSerializer(data = request.data)
    if serializer.is_valid():
        if len( Users.objects.filter(email=serializer.data['email']).all() ) !=0:
            return Response("email already taken")
        else:
            usermail = serializer.data['email']
            usercollege = serializer.data['college']
            userbranch = serializer.data['branch']
            userfullname = serializer.data['fullname']

            pwo = PasswordGenerator()
            pwo.minlen = 30
            pwo.maxlen = 40
            hashkey=pwo.generate()
            issend = send_mail(f"Welcome {userfullname}", f"{hashkey}      is your validation key, Don't share it with anyone!!", 'khushimorankar96@gmail.com', [f"{usermail}"])
            if issend!=1:
                return Response("email is invalid!!")
            userhashkey = hashkey
            user = Users(email=usermail, college= usercollege, branch = userbranch, fullname = userfullname, hashkey = userhashkey)
            user.save() 


    # email = request.POST['email'] 
    
    return Response("Hey!! your post is succesfully created once reviewed it will be live on our website!!")

@api_view(['GET'])
def requestkey(request,email):
    user = Users.objects.filter(email=email)
    if len(user)==0:
        return Response("email is not registered yet!! please register your email")
    else:
        user = user[0]
        pwo = PasswordGenerator()
        pwo.minlen = 30
        pwo.maxlen = 40
        hashkey=pwo.generate()
        issend = send_mail(f"Welcome back {user.fullname} !!", f"{hashkey}      is your validation key, Don't share it with anyone!!", 'khushimorankar96@gmail.com', [f"{user.email}"])
        
        user.hashkey = hashkey
        user.save()

    

    return Response("Verification key is send to your email please check!!")
    