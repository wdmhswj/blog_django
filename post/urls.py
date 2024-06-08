from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('', views.IndexView,name = 'my_blog'),
    path('page/<int:page_number>', views.IndexView,name='index_page'),
    path('<int:pk>', views.DetailView, name='post_detail'),
    path('category/<int:category_id>', views.getPostByCid, name='category_posts'),
    path('archive/<int:year>/<int:month>', views.getPostByCreated, name='archive_posts'),
    path('archive/', views.getPostByCreated, name='all_archive_posts'),
    
    
]

