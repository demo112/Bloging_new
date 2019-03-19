# View视图初探

\**Django 中的视图的概念是「一类具有相同功能和模板的网页的集合」。**比如，在一个博客应用中，你可能会创建如下几个视图：

* 博客首页：展示最近的几项内容。
* 内容“详情”页：详细展示某项内容。
* 评论处理器：用于响应为一项内容添加评论的操作。

这些需求都靠**视图（View）**来完成。

# Hello World!

首先写一个最简单的**视图函数**，在浏览器中打印出`Hello World!`字符串。

打开`article/views.py`，写出视图函数：

```hljs
article/views.py

# 导入 HttpResponse 模块
from django.http import HttpResponse

# 视图函数
def article_list(request):
    return HttpResponse("Hello World!")
复制代码
```

\**在 Django 中，网页都是从视图派生而来。**每一个视图表现为一个简单的 Python 函数，它必须要做的只有两件事：返回一个包含被请求页面内容的 `HttpResponse`对象，或者抛出一个异常，比如 `Http404` 。至于你还想干些什么，随便你。

视图函数中的`request`与网页发来的请求有关，里面包含get或post的内容、用户浏览器、系统等信息。Django调用`article_list`函数时会返回一个含字符串的 `HttpResponse`对象。

\**有了视图函数，还需要配置URLconfs，将用户请求的URL链接关联起来。**换句话说，URLconfs的作用是将URL映射到视图中。

在[前面的文章](https://link.juejin.im/?target=https%3A%2F%2Fwww.dusaiphoto.com%2Farticle%2Farticle-detail%2F6%2F)中已经将项目`/article`的URL分发给了`article`应用，因此这里只需要修改之前添加的`article/urls.py`就可以。添加以下代码：

```hljs
article/urls.py

# 引入views.py
from . import views

...

urlpatterns = [
    # path函数将url映射到视图
    path('article-list/', views.article_list, name='article_list'),
]
复制代码
```

\**Django 将会根据用户请求的 URL 来选择使用哪个视图。**本例中当用户请求`article/article-list`链接时，会调用`views.py`中的`article_list`函数，并返回渲染后的对象。参数`name`用于反查url地址，相当于给url起了个名字，以后会用到。

**测试一下刚才敲的代码是否工作正常。**

**在虚拟环境中**，进入项目目录，也就是`my_blog`文件夹，输入`python manage.py runserver`，运行调试服务器：

```hljs
(env) E:\django_project\my_blog>python manage.py runserver

Performing system checks...

System check identified no issues (0 silenced).
August 30, 2018 - 19:41:00
Django version 2.1, using settings 'my_blog.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
复制代码
```

成功运行后，打开浏览器，输入url地址`http://127.0.0.1:8000/article/article-list/`，其中`127.0.0.1:8000`是调试服务器的本地地址，`article`是项目路由`my_blog\urls.py`分发的地址，`article-list`是刚才配置的`article\urls.py`应用分发的地址。

运气好的话，浏览器中会打印出`Hello World!`字符串：

<figure>![](data:image/svg+xml;utf8,<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="429"></svg>)
<figcaption></figcaption></figure>

**不到10行代码就完成了基本功能，是不是很神奇。**

当然，只是小试牛刀。

# 准备工作

在前面章节[编写Model模型](https://link.juejin.im/?target=https%3A%2F%2Fwww.dusaiphoto.com%2Farticle%2Farticle-detail%2F11%2F)中虽然定义了数据库表，但是这个表是空的，不方便展示View调取数据的效果。所以在写View之前，需要往数据表里记录一些数据。接下来就做这个工作。

## 网站后台概念

**网站后台**，有时也称为**网站管理后台**，是指用于管理网站的一系列操作，如：数据的增加、更新、删除等。在项目开发的初期，因为没有真实的用户数据和完整的测试环境，会频繁地使用后台修改测试数据。

幸运的是Django内置了一个很好的后台管理工具，只需要些少量代码，就可以实现强大的功能。

## 创建管理员账号（Superuser）

管理员账号（Superuser）是可以进入网站后台，对数据进行维护的账号，具有很高的权限。这里我们需要创建一个管理员账号，以便添加后续的测试数据。

**虚拟环境**中输入`python manage.py createsuperuser`指令，创建管理员账号：

```hljs
(env) E:\django_project\my_blog>python manage.py createsuperuser
Username: dusai
Email address: dusaiphoto@foxmail.com
Password:
Password (again):
Superuser created successfully.
复制代码
```

指令会提示你输入账号名字、邮箱和密码，根据喜好填入即可创建成功。

## 将ArticlePost注册到后台中

接下来我们需要“告诉”Django，后台中需要添加`ArticlePost`这个数据表供管理。

打开`article/admin.py`，写入以下代码：

```hljs
article/admin.py

from django.contrib import admin

# 别忘了导入ArticlerPost
from .models import ArticlePost

# 注册ArticlePost到admin中
admin.site.register(ArticlePost)
复制代码
```

这样就简单的注册好了。

## 在后台中遨游

细心的同学可能已经发现，Django项目生成的时候就自动配置好了后台的settings和url，因此不需要我们再操心了。

启动server，在浏览器中输入`http://127.0.0.1:8000/admin/`，一切正常的话就看到下面的登录界面了：

<figure>![](data:image/svg+xml;utf8,<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="800" height="404"></svg>)
<figcaption></figcaption></figure>

输入刚才创建的管理员账号，登录进去：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e8415265594?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

红框内就是刚才添加的`ArticlePost`数据表，点击进入后，再点击右上角的`ADD ARTICLE POST`按钮，到达如下页面：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e84447af87e?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

仔细看一下表单中的每一项，发现与`ArticlePost`中的字段完全符合；因为`updated`字段指定了自动添加，这里就没显示了。

将表单填好后，点击保存：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e8412e13f29?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

可以看到ARTICLE POST中多了刚才录入的一条数据。按照同样的方法，再写入几条数据：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e844e86ed8b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

至此准备工作就已经大功告成。

# 检视数据库

> 2018-10-29 新增内容

通过上面的操作，我们的数据库中已经有1条用户数据、3条文章数据了。有的时候我需要检查数据库中的数据是否正确，但是项目中的数据库文件`db.sqlite3`又无法直接打开，怎么办呢？

这时候就需要用到专门处理SQLite数据文件的软件了：[SQLiteStudio](https://link.juejin.im/?target=https%3A%2F%2Fsqlitestudio.pl%2Findex.rvt)

下载并安装，用它打开`db.sqlite3`，软件导航栏中就出现了数据库中保存的各类数据列表。比如说auth_user就是用户数据表了：

<figure>![](https://user-gold-cdn.xitu.io/2018/10/29/166c0257020d0078?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

你可以用它检查项目代码中数据库的操作是否正常，这在开发阶段是非常实用的。

# 