from django.contrib import admin
from restapi.models import Blog, Users, Admin

# Register your models here.
admin.site.register(Blog)
admin.site.register(Users)
admin.site.register(Admin)