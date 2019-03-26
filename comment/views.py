from django.shortcuts import render, redirect, get_object_or_404
from article.models import ArticlePost
from .forms import CommentForm


# Create your views here.
def post_comment(request, article_id):
    try:
        article = get_object_or_404(ArticlePost, id=article_id)
    except Exception as e:
        return redirect('err:not_found', e=e)
    if request.method == "POST":
        # 将表单内容写入到评论类中
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            #  如果数据符合格式
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()
            return redirect(article)
        else:
            return redirect('err:wrong_input')
    else:
        return redirect('err:wrong_method')
