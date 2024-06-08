"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from post import views
# from post.admin import admin_site
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path("admin/", admin_site.urls),
    path("admin/", admin.site.urls),
    path("post/", include('post.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # path('search/', include('haystack.urls')),
    # path("post/", views.IndexView,name = 'my_blog'),
    path('', views.choose_view, name='choose'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('success/', views.success_view, name='success'),
    path('register/', views.register_view, name='register'),
    path('aboutme/', views.aboutme_view),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search_view, name='search'),
    path('show_post/<int:post_id>/', views.show_post, name='post_detail'),
    path('show_user/<int:user_id>/<int:page_id>', views.show_user, name='show_user'),
    path("tips/", views.tips_view),
]
