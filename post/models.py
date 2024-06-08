from django.db import models
from django.utils.text import Truncator
# Create your models here.

class Category(models.Model):
    cname = models.CharField(max_length=30, unique=True, verbose_name='类别名称')

    def __str__(self):
        return f'<类别:{self.cname}>'

    class Meta:
        db_table = 't_category'
        verbose_name_plural = '类别'


class Tag(models.Model):
    tname = models.CharField(max_length=20, unique=True, verbose_name='标签名称')

    def __str__(self):
        return f'<标签:{self.tname}>'

    class Meta:
        db_table = 't_tag'
        verbose_name_plural = '标签'


from ckeditor.fields import RichTextField
from django.contrib.auth.models import User


class Post(models.Model):
    user = models.ForeignKey(User, verbose_name='用户名', default=1,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, unique=True, verbose_name='标题')
    desc = models.CharField(max_length=200, verbose_name='简介')
    content = RichTextField(verbose_name='内容')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    isdelete = models.BooleanField(default=False, verbose_name='是否删除')
    category = models.ForeignKey(Category, verbose_name='所属类别',default=1, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='所属标签')
    
    def __str__(self):
        return f'<帖子:{self.title}>'

    class Meta:
        db_table = 't_post'
        verbose_name_plural = '帖子'

from django.contrib.auth.models import Group

group, created = Group.objects.get_or_create(name='Common User')
if created==True:
    group.save()


from django import forms
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'desc', 'content', 'category', 'tag']