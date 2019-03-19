# 渲染Markdown文章目录

对会读书的人来说，读一本书要做的第一件事，就是仔细阅读这本书的目录。阅读目录可以对整体内容有所了解，并清楚地知道感兴趣的部分在哪里，提高阅读质量。

博文也是同样的，好的目录对博主和读者都很有帮助。更进一步的是，还可以在目录中设置锚点，点击标题就立即前往该处，非常的方便。

# 文中的目录

之前我们已经为博文支持了Markdown语法，现在继续增强其功能。

有折腾代码高亮的痛苦经历之后，设置Markdown的目录扩展就显得特别轻松了。

修改文章详情视图：

```
article/views.py

...

# 文章详情
def article_detail(request, id):
    ...
    article.body = markdown.markdown(article.body,
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
            
        # 目录扩展
        'markdown.extensions.TOC',
        ]
    )
    ...
复制代码
```

仅仅是将将`markdown.extensions.TOC`扩展添加了进去。

> TOC: Table of Contents，即目录的意思

代码增加这一行就足够了。为了方便测试，往之前的文章中添加几个一级标题、二级标题等。

> 还记得Markdown语法如何写标题吗？一级标题：`# title1`，二级标题：`## title2`

然后你可以在文中的任何地方插入`[TOC]`字符串，目录就自动生成好了：



![img](data:image/svg+xml;utf8,<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1200" height="726"></svg>)



点击标题，页面就立即前往相应的标题处（即“锚点”的概念）。

# 任意位置的目录

上面的方法只能将目录插入到文章当中。如果我想把目录插入到页面的任何一个位置呢？

也简单，这次需要修改Markdown的渲染方法：

```
article/views.py

...

def article_detail(request, id):
    ...

    # 修改 Markdown 语法渲染
    md = markdown.Markdown(
        extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        ]
    )
    article.body = md.convert(article.body)

    # 新增了md.toc对象
    context = { 'article': article, 'toc': md.toc }

    return render(request, 'article/detail.html', context)
复制代码
```

为了能将`toc`单独提取出来，我们先将Markdown类赋值给一个临时变量`md`，然后用`convert()`方法将正文渲染为html页面。通过`md.toc`将目录传递给模板。

> 注意`markdown.markdown()`和`markdown.Markdown()`的区别
>
> 更详细的解释见：[官方文档](https://link.juejin.im/?target=https%3A%2F%2Fpython-markdown.github.io%2Fextensions%2Ftoc%2F)

为了将新的目录渲染到页面中，需要修改文章详情模板：

```
templates/article/detail.html

...

<div class="container">
    <div class="row">
        <!-- 将原有内容嵌套进新的div中 -->
        <div class="col-9">
            <h1 class="mt-4 mb-4">{{ article.title }}</h1>
            <div class="alert alert-success">
                ...
            </div>
        </div>

        <!-- 新增的目录 -->
        <div class="col-3 mt-4">
            <h4><strong>目录</strong></h4>
            <hr>
            <div>
                {{ toc|safe }}
            </div>
        </div>
    </div>
</div>

...
复制代码
```

- 重新布局，将原有内容装进`col-9`的容器中，将右侧`col-3`的空间留给目录
- `toc`需要`|safe`标签才能正确渲染

重新打开页面：



![img](https://user-gold-cdn.xitu.io/2019/1/1/1680842d14f33a8d?imageView2/0/w/1280/h/960/format/webp/ignore-error/1)



# 总结

完成了文章的目录功能，至此文章详情页面也比较完善了。

- 有疑问请在[杜赛的个人网站](https://link.juejin.im/?target=http%3A%2F%2Fwww.dusaiphoto.com)留言，我会尽快回复。
- 或Email私信我：dusaiphoto@foxmail.com
- 项目完整代码：[Django_blog_tutorial](https://link.juejin.im/?target=https%3A%2F%2Fgithub.com%2Fstacklens%2Fdjango_blog_tutorial)

> 转载请注明出处。