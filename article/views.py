import random

import markdown as markdown
from .models import ArticlePost
# 引入redirect重定向模块
from django.shortcuts import render, redirect, render_to_response
# 引入HttpResponse
from django.http import HttpResponse
# 引入刚才定义的ArticlePostForm表单类
from .forms import ArticlePostForm
# 引入User模型
from django.contrib.auth.models import User
from django.core.paginator import Paginator


def article_order(request, order):
    url = request.META['HTTP_REFERER']
    print(url)
    response = redirect('article:article_list')
    response.set_cookie('order', order, 60 * 60 * 10)
    return response


# Create your views here.
def article_list(request):
    order = request.COOKIES['order']
    print(order)
    # 取出所有博客文章
    articles_list = ArticlePost.objects.all().order_by('-' + order)
    # 每页显示的文章，每页最少，可以首页为空
    paginator = Paginator(articles_list, 6, 3, True)
    # 获取 url 中的页码
    page = request.GET.get('page')
    # 将导航对象相应的页码内容返回给 articles
    articles = paginator.get_page(page)

    # todo 需要传递给模板（templates）的对象
    # styles = ["bg-primary", "bg-secondary", "bg-success", "bg-danger", "bg-warning", "bg-info", "bg-dark"]
    # style = styles[random.random(len(styles))]
    context = {'articles': articles}
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)
    # todo 使用另一种博客预览
    # return render(request, 'article/list_img.html', context)


def article_detail(request, article_id):
    try:
        article = ArticlePost.objects.get(id=article_id)
        # 将markdown语法渲染成html样式
        article.body = markdown.markdown(
            article.body,
            extensions=[
                # 包含 缩写、表格等常用扩展
                'markdown.extensions.extra',
                # 语法高亮扩展
                'markdown.extensions.codehilite',
            ])
        context = {'article': article}
        # 增加阅读量
        # todo 解决无登陆刷新也可以增加的问题
        print(request.GET)
        if not article.author.id == request.user.id:
            article.total_views += 1
            article.save(update_fields=['total_views'])
        return render(request, 'article/detail.html', context)
    except Exception as e:
        return redirect('err:not_found', e=e)


def article_create(request):
    if request.user.id:
        pass
    else:
        return redirect('userprofile:login')
    # 判断用户是否提交数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存数据，但暂时不提交到数据库中
            new_article = article_post_form.save(commit=False)
            # 指定数据库中作者的用户id
            new_article.author = User.objects.get(id=request.user.id)
            # 将新文章保存到数据库中
            new_article.save()
            # 完成后返回到文章列表
            return redirect("article:article_list")
        # 如果数据不合法，返回错误信息
        else:
            return redirect('err:wrong_input', e='表单内容有误~')
    # 如果用户请求获取数据
    elif request.method == "GET":
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文
        context = {'article_post_form': article_post_form}
        # 返回模板
        return render(request, 'article/create.html', context)
    else:
        return redirect('err:wrong_method')


def article_delete(request, article_id):
    try:
        # 根据 id 获取需要删除的文章
        article = ArticlePost.objects.get(id=article_id)
        # 调用.delete()方法删除文章
        article.delete()
        # 完成删除后返回文章列表
        return redirect("article:article_list")
    except Exception as e:
        return redirect('err:not_found', e=e)


def article_update(request, article_id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """

    # 获取需要修改的具体文章对象
    article = ArticlePost.objects.get(id=article_id)
    # 鉴权
    if request.user != article.author:
        redirect('err:no_permission')
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticlePostForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['body']
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 article_id 值
            return redirect("article:article_detail", article_id=article_id)
        # 如果数据不合法，返回错误信息
        else:
            return redirect('err:wrong_input')

    # 如果用户 GET 请求获取数据
    elif request.method == "GET":
        # 创建表单类实例
        article_post_form = ArticlePostForm()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {'article': article, 'article_post_form': article_post_form}
        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
    else:
        return redirect('err:wrong_method')
