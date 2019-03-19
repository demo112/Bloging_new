# 创建并配置APP功能模块

# 创建APP

\**在Django中的一个app代表一个功能模块。**开发者可以将不同功能的模块放在不同的app中, 方便代码的复用。app就是项目的基石，因此开发博客的第一步就是创建新的app，用来实现跟文章相关的功能模块。

打开命令行，进入项目所在的目录：**（注意Django的操作必须在虚拟环境下进行）**

```hljs
E:\>cd django_project
E:\django_project>
复制代码
```

进入虚拟环境（忘记进入venv方法的看这里： [在Windows中搭建Django的开发环境](https://link.juejin.im/?target=http%3A%2F%2Fwww.dusaiphoto.com%2Farticle%2Farticle-detail%2F4%2F)）：

```hljs
E:\django_project> env\Scripts\activate.bat
(env) E:\>
复制代码
```

看到盘符前有`(env)`标识则表示进入虚拟环境成功。

输入`python manage.py startapp article`指令，创建名为`article`的app：

```hljs
(env) E:\django_project\my_blog>python manage.py startapp article
复制代码
```

查看一下`my_blog`文件夹，应该看到这样的结构：

```hljs
my_blog
│  db.sqlite3
│  manage.py
│
├─article
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  └─migrations
│          __init__.py
│
└─my_blog
    │  settings.py
    │  urls.py
    │  wsgi.py
    └─ __init__.py
复制代码
```

其中`article`文件夹就是刚创建出来的app，用来放置博客文章相关的代码。

# 注册APP（settings）

**接着我们需要修改项目配置文件，“告诉”Django现在有article这么一个app了。**

打开根目录的`settings.py`，找到`INSTALLED_APPS`写入如下代码：

```hljs
settings.py/

INSTALLED_APPS = [
	# 其他代码
	...

	# 新增'article'代码，激活app
    'article',
]
复制代码
```

# 配置访问路径（urls）

**然后再给app配置访问路径url。**

url可以理解为访问网站时输入的网址链接，配置好url后Django才知道怎样定位app。

打开根目录下的`urls.py`，增加以下代码：

```hljs
urls.py/

from django.contrib import admin
# 记得引入include
from django.urls import path, include

# 存放映射关系的列表
urlpatterns = [
    path('admin/', admin.site.urls),

    # 新增代码，配置app的url
    path('article/', include('article.urls', namespace='article')),
]

复制代码
```

`path`为Django的路由语法。参数`article/`分配了app的访问路径；`include`将路径分发给下一步处理；`namespace`可以保证反查到唯一的url，即使不同的app使用了相同的url（后面会用到）。**记得在顶部引入`include`。**

\**还没结束。**现在我们已经通过`path`将根路径为`article/`的访问都分发给article这个app去处理。但是app通常有多个页面地址，因此还需要app自己也有一个路由分发，也就是`article.urls`了。

在app生成时并没有这个文件，因此需要自己在`article/`文件夹中创建`urls.py`，在里面输入：

```hljs
article/urls.py

# 引入path
from django.urls import path

# 正在部署的应用的名称
app_name = 'article'

urlpatterns = [
    # 目前还没有urls
]
复制代码
```

`urlpatterns`中暂时是空的，没写入任何路径的映射，不着急以后会写。

**注意Django2.0之后，app的`urls.py`必须配置`app_name`，否则会报错。**

此时我们的app就配置完成了。