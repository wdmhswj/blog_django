from django.contrib import admin
from .models import *
# Register your models here.




# class MyAdminSite(admin.AdminSite):
#     site_url = "/post"
#     # pass

# admin_site = MyAdminSite(name="admin")
# admin_site.register(Category)
# admin_site.register(Tag)
# admin_site.register(Post)

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
