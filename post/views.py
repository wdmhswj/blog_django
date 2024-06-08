
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,authenticate
from django.shortcuts import render,redirect,get_object_or_404

# Create your views here.

from django.views import View
from .models import *
from django.core.paginator import Paginator
import math

from .forms import UserRegistrationForm, SearchForm
from django.db.models import Q

@login_required
def IndexView(request,page_number=1):
    # 获取当前登录用户
    user = request.user
    
    num = int(page_number)

    #查询数据库中所有的贴子信息
    postList = Post.objects.filter(user=user).all().order_by('-created')
    #创建分页器对象
    page_obj = Paginator(postList,3)
    #获取某一页数据
    page_post = page_obj.page(num)

    #获取每一页显示页码数列表[2,...,11]
    begin = num - int(math.ceil(10.0/2))
    if begin <1:
        begin =1
    end = begin + 9
    if end > page_obj.num_pages:
        end = page_obj.num_pages

    if end <10:
        begin = 1
    else:
        begin = end -9

    page_list = range(begin,end+1)

    return render(request,'index.html',{'postList':page_post,'page_list':page_list,'currentNum':num})

def DetailView(request,pk):
    postid = int(pk)

    post_obj = Post.objects.get(id=postid)

    return render(request,'detail.html',{'post_obj':post_obj})


def choose_view(request):
    return render(request, 'choose.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # 登录用户
            login(request, form.get_user())
            return redirect('my_blog')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


# def register_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password == confirm_password:
#             # 检查用户名是否已存在
#             if User.objects.filter(username=username).exists():
#                 return render(request, 'register.html', {'error': '用户名已存在'})
#             else:
#                 # 创建超级用户
#                 # User.objects.create_superuser(username=username, password=password)
#                 # 使用创建的超级用户进行登录
#                 # user = authenticate(username=username, password=password)
#                 if user is not None:
#                     login(request, user)        # 注册成功后自动登录
#                     return render(request, 'success.html')
#         else:
#             return render(request, 'register.html', {'error': '密码不匹配'})

#     return render(request, 'register.html')

def register_view(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():        # User模型中username字段是唯一的，is_valid()会进行检查
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            
            # 将 is_staff 属性设置为True
            new_user.is_staff=True

            # Save the User object
            new_user.save()

            # 获取先前创建的组或创建新组
            group, created = Group.objects.get_or_create(name='Common User')
            if created==False:
                # 将用户添加到组中
                new_user.groups.add(group)

            # Create the user profile
            # Profile.objects.create(user=new_user)
            return render(request,
                          'success.html')
    else:
        user_form = UserRegistrationForm()      # 空表单
    return render(request,
                  'register.html',
                  {'user_form': user_form})


def getPostByCid(request,category_id=1):
    category_id = int(category_id)

    c_post = Post.objects.filter(category__id=category_id)

    return render(request,'postlist.html',{'c_post':c_post})


def getPostByCreated(request,year=1,month=1):
    year = int(year)
    month = int(month)

    if year==1 and month ==1:
        c_post = Post.objects.all().order_by('-created')
    else:
        c_post = Post.objects.filter(created__year=year,created__month=month)

    return render(request, 'postlist.html', {'c_post': c_post})

def aboutme_view(request):
    return render(request, 'aboutme.html')

from django.contrib import messages
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # 设置帖子的作者为当前登录的用户
            post.save()
            form.save_m2m()  # 保存多对多关系

            messages.success(request, '帖子创建成功！')  # 添加成功消息
            return redirect('/post/')  # 重定向到 '/post/' URL
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def search_view(request):
    # 搜索结果展示
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            # 获取关键字
            keywords = form.cleaned_data['keywords']
            # 构建查询语句
            query = Q(title__icontains=keywords) | \
                    Q(desc__icontains=keywords) | \
                    Q(content__icontains=keywords) |\
                    Q(user__username__icontains=keywords)
            # 查询过滤
            results = Post.objects.filter(query)
            # users = User.objects.filter(username__icontains=username)
            return render(request, 'search.html',
                           {'form': form,
                            'results': results})
    
    # 默认展示
    else:
        form = SearchForm() # 空表单
        # 获取最近创建的8个帖子
        recent_posts = Post.objects.filter(isdelete=False).order_by('-created')[:8]
    # return render(request,'show.html')
    return render(request, 'search.html', 
                  {'form': form,
                   'recent_posts': recent_posts})

def show_post(request, post_id):
    # 获取帖子对象，如果不存在则返回 404
    post = get_object_or_404(Post, id=post_id)

    # 渲染帖子内容页面模板，将帖子对象传递给模板
    return render(request, 'show_post.html', {'post_obj': post})

def show_user(request, user_id, page_id=1):
    user=get_object_or_404(User, id=user_id)
    username=user.username
    #查询数据库中所有的贴子信息
    postList = Post.objects.filter(user=user_id).all().order_by('-created')
    #创建分页器对象
    page_obj = Paginator(postList,3)
    #获取某一页数据
    page_post = page_obj.page(page_id)

    #获取每一页显示页码数列表[2,...,11]
    begin = page_id - int(math.ceil(10.0/2))
    if begin <1:
        begin =1
    end = begin + 9
    if end > page_obj.num_pages:
        end = page_obj.num_pages

    if end <10:
        begin = 1
    else:
        begin = end -9

    page_list = range(begin,end+1)

    return render(request,'show_user.html',
                  {'postList':page_post,
                   'page_list':page_list,
                   'currentNum':page_id,
                   'username':username})

def success_view(request):
    return render(request,'success.html')

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return render(request,'registration/logout.html')

def tips_view(request):
    return render(request,'tips.html')