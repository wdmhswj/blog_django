#coding=utf-8
from django.db.models import Count

from .models import *
from django.db import connection



def getRightInfo(request):
    #分类
    r_cate_post = Post.objects.values('category__cname','category').annotate(c=Count('*')).order_by('-c')


    #近期文章
    r_recent_post = Post.objects.order_by('-created')[:3]

    cursor = connection.cursor()
    r_file_post = cursor.execute('select created,count("*") count from t_post GROUP by strftime("%Y-%m",created) order by count desc ')

    return {'r_cate_post':r_cate_post,'r_recent_post':r_recent_post,'r_file_post':r_file_post}

def getHeaderInfo(request):
    user = request.user

    return {'user':user}