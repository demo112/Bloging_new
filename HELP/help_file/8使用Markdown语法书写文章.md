# 使用Markdown语法书写文章

上一章我们实现了文章详情页面。为了让文章正文能够进行标题、加粗、引用、代码块等不同的排版（像在Office中那样！），我们将使用Markdown语法。

# 安装Markdown

**Markdown**是一种轻量级的标记语言，它允许人们“使用易读易写的纯文本格式编写文档，然后转换成有效的或者HTML文档。建议读者一定要花五分钟时间熟悉一下Markdown的语法，熟练后码字效率一定会大幅提高。

关于Markdown语法看这里：[Markdown 语法介绍](https://link.juejin.im/?target=https%3A%2F%2Fcoding.net%2Fhelp%2Fdoc%2Fproject%2Fmarkdown.html)

安装markdown也很简单：进入虚拟环境，输入指令`pip install markdown`即可。

# 使用Markdown

为了将Markdown语法书写的文章渲染为HTML文本，首先改写`article/views.py`的`article_detail()`：

```hljs
article/views.py

...

# 引入markdown模块
import markdown

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    # 将markdown语法渲染成html样式
    article.body = markdown.markdown(article.body,
        extensions=[
        # 包含 缩写、表格等常用扩展
        'markdown.extensions.extra',
        # 语法高亮扩展
        'markdown.extensions.codehilite',
        ])

    context = { 'article': article }
    return render(request, 'article/detail.html', context)
复制代码
```

代码中`markdown.markdown`语法接收两个参数：第一个参数是需要渲染的文章正文`article.body`；第二个参数载入了常用的语法扩展，`markdown.extensions.extra`中包括了缩写、表格等扩展，`markdown.extensions.codehilite`则是后面要使用的代码高亮扩展。

然后，修改`templates/article/detail.html`中有关文章正文的部分：

```hljs
templates/article/detail.html

...

# 在 article.body 后加上 |safe 过滤器
<p>{{ article.body|safe }}</p>
复制代码
```

Django出于安全的考虑，会将输出的HTML代码进行转义，**这使得`article.body`中渲染的HTML文本无法正常显示。**管道符`|`是Django中过滤器的写法，而`|safe`就类似给`article.body`贴了一个标签，表示这一段字符不需要进行转义了。

这样就把Markdown语法配置好了。

启动服务器，在后台中新录入一条用markdown语法书写的文章，内容如下：

```hljs
# 国风·周南·关雎
---
**关关雎鸠，在河之洲。窈窕淑女，君子好逑。**

参差荇菜，左右流之。窈窕淑女，寤寐求之。

---
+ 列表一
+ 列表二
    + 列表二-1
    + 列表二-2
---

​```python
def article_detail(request, id):
	article = ArticlePost.objects.get(id=id)
	# 将markdown语法渲染成html样式
	article.body = markdown.markdown(article.body,
		extensions=[
		# 包含 缩写、表格等常用扩展
		'markdown.extensions.extra',
		# 语法高亮扩展
		'markdown.extensions.codehilite',
		])
	context = { 'article': article }
	return render(request, 'article/detail.html', context)
```
复制代码
```

返回文章详情，结果如下：

<figure>![](data:image/svg+xml;utf8,<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1200" height="733"></svg>)
<figcaption></figcaption></figure>

很好，但是代码块还是不怎么好看。

写技术文章没有代码高亮怎么行。继续努力。

# 代码高亮

在`static`目录中新建一个目录`md_css/`，一会儿放置代码高亮的样式文件。

重新打开一个命令行窗口，**进入虚拟环境，安装Pygments：`pip install Pygments`**

Pygments是一种通用语法高亮显示器，可以帮助我们自动生成美化代码块的样式文件。

在命令行中进入刚才新建的`md_css`目录中，输入Pygments指令：

​```hljs
pygmentize -S monokai -f html -a .codehilite > monokai.css
复制代码
```

**这里有一点需要注意, 生成命令中的 -a 参数需要与真实页面中的 CSS Selector 相对应，即`.codehilite`这个字段在有些版本中应写为`.highlight`。如果后面的代码高亮无效，很可能是这里出了问题。**

回车后检查一下，在`md_css`目录中是否自动生成了一个叫`monokai.css`的文件，这是一个深色背景的高亮样式文件。

接下来我们在`base.html`中引用这个文件：

```hljs
templates/base.html

<head>
    ...
    <link rel="stylesheet" href="{% static 'bootstrap/css/bootstrap.min.css' %}">

    <!-- 引入monikai.css -->
    <link rel="stylesheet" href="{% static 'md_css/monokai.css' %}">

</head>
...
复制代码
```

重新启动服务器，顺利的话看到如下：

<figure>![](https://user-gold-cdn.xitu.io/2018/9/29/16624eab5f27222b?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)
<figcaption></figcaption></figure>

除了Monokai这个深色的样式外，Pygments还内置了很多其他的样式，这个就看喜好选择了。

各种不同样式可以在这里参照：[pygments-css](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Frichleland%2Fpygments-css)