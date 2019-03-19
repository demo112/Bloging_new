import markdown as markdown
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import ArticlePost


# Create your views here.
def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
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
        return render(request, 'article/detail.html', context)
    except Exception as e:
        return redirect('err:not_found', e=e)
