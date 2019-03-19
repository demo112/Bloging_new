# 改写View视图

# 改写视图函数

上一章我们感受了视图的工作流程。

\**为了让视图真正发挥作用，**改写`article/views.py`中的`article_list`视图函数：

```hljs
article/views.py

from django.shortcuts import render

# 导入数据模型ArticlePost
from .models import ArticlePost

def article_list(request):
    # 取出所有博客文章
    articles = ArticlePost.objects.all()
    # 需要传递给模板（templates）的对象
    context = { 'articles': articles }
    # render函数：载入模板，并返回context对象
    return render(request, 'article/list.html', context)
复制代码
```

代码同样很直白，分析如下：

* `.models`表示从当前文件夹的`models.py`文件中导入`ArticlePost`数据类
* `ArticlePost.objects.all()`从`ArticlePost`数据类获得所有的对象（即博客文章），并传递给`articles`变量
* `context`定义了需要传递给模板的对象，即`articles`
* 最后返回了`render`函数：

    * 第一个变量是固定的`request`对象，照着写就可以
    * 第二个变量定义了模板文件的位置、名称，即`article/list.html`
    * 第三个变量定义了需要传入模板文件的对象，即`context`

视图函数这样就写好了。

# 编写模板（template）

在前面的视图中我们定义了模板的位置在`article/list.html`，因此在根目录下新建`templates`文件夹，再新建`article`文件夹，再新建`list.html`文件，即：

```hljs
my_blog
│  ...
├─article
│  ...
└─my_blog
│  ...
└─templates
    └─ article
        └─ list.html
复制代码
```

细心的你肯定注意到了，之前的Django文件后缀都是`.py`，代表Python文件；这里的模板文件后缀是`.html`，这又是什么呢？

\**HTML是一种用于创建网页的标记语言。**它被用来结构化信息，标注哪些文字是标题、哪些文字是正文等（当然不仅仅这点功能）。也可以简单理解为“给数据排版”的文件，跟你写文档用的Office Word一样一样的 。

在`list.html`文件中写入：

```hljs
templates/article/list.html

{% for article in articles %}
	<p>{{ article.title }}</p>
{% endfor %}
复制代码
```

作为一个Web框架，Django通过模板来动态生成HTML，其中就包含描述动态内容的一些特殊语法：

* `{% for article in articles %}`：`articles`为视图函数的`context`传递过来的对象，即所有文章的集合。`{% for %}`循坏表示依次取出`articles`中的元素，命名为`article`，并分别执行接下来操作。末尾用`{% endfor %}`告诉Django循环结束的位置。

* 使用`.`符号来访问变量的属性。这里的`article`为模型中的某一条文章；我们在前面的`ArticlePost`中定义了文章的标题叫`title`，因此这里可以用`article.title`来访问文章的标题。

* `<p>...</p>`即为html语言，中间包裹了一个段落的文字。

**在上一章中已经定义好了`urls.py`，因此不再需要改动。**

一切都很好，深吸一口气。保存所有文件，在浏览器中输入地址`http://127.0.0.1:8000/article/article-list/`，得到以下错误：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e8d13458961?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

似乎成功从来都不会很顺利。

# 错误分析

虽然出错了，但幸运的是Django提供了非常完善的错误处理系统，方便开发者快速找到Bug的蛛丝马迹。

第一行就醒目地提示：**TemplateDoesNotExist**，说明Django没有找到`list.html`这个文件。仔细检查目录、文件的名称无误，没问题就往下继续看。

然后发现有这么两行：

```hljs
...django\contrib\admin\templates\article\list.html (Source does not exist)
...django\contrib\auth\templates\article\list.html (Source does not exist)
复制代码
```

似乎Django在这两个位置搜索，没有发现需要的文件，然后返回了“未发现模板文件”的错误。

定位了问题的所在，接下来就是在哪里“告诉”Django我的模板的位置呢？

**答案就在`settings.py`中了，它保存了Django项目的各种初始配置。**

打开并找到这一段，加入代码`os.path.join(BASE_DIR, 'templates')`：

```hljs
my_blog/settings.py

TEMPLATES = [
    {
        ...
        # 定义模板位置
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        ...
    },
]
复制代码
```

这就是说模板文件在项目根目录的`templates`文件夹中，去找找吧。

很好，保存文件，重新启动服务器，刷新浏览器，如下：

---

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624e8d008b36ab?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>
---

成功！

虽然简陋，但是已经完全走通了MTV（model、template、view）整个环路。

不要激动，精彩的还在后面。