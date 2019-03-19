# 编写博客文章的Model模型

**Django 框架主要关注的是模型（Model）、模板（Template）和视图（Views），称为MTV模式。**

它们各自的职责如下：

| 层次                           | 职责                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| 模型（Model），即数据存取层    | 处理与数据相关的所有事务： 如何存取、如何验证有效性、包含哪些行为以及数据之间的关系等。 |
| 模板（Template），即业务逻辑层 | 处理与表现相关的决定： 如何在页面或其他类型文档中进行显示。  |
| 视图（View），即表现层         | 存取模型及调取恰当模板的相关逻辑。模型与模板的桥梁。         |

**简单来说就是Model存取数据，View决定需要调取哪些数据，而Template则负责将调取出的数据以合理的方式展现出来。**

在 Django 里写一个数据库驱动的 Web 应用的第一步是定义**模型Model**，也就是数据库结构设计和附加的其它元数据。

模型包含了储存的数据所必要的字段和行为。Django 的目标是你只需要定义数据模型，其它的杂七杂八代码你都不用关心，它们会自动从模型生成。

所以让我们首先搞定**Model**。

## 编写 Model

**如前面所讲，Django中通常一个模型（Model）映射一个数据库，处理与数据相关的事务。**

对博客网站来说，最重要的数据就是文章。所以首先来建立一个存放文章的数据模型。

打开`article/models.py`文件，输入如下代码：

```hljs
article/models.py

from django.db import models
# 导入内建的User模型。
from django.contrib.auth.models import User
# timezone 用于处理时间相关事务。
from django.utils import timezone

# 博客文章数据模型
class ArticlePost(models.Model):
    # 文章作者。参数 on_delete 用于指定数据删除的方式，避免两个关联表的数据不一致。
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # 文章标题。models.CharField 为字符串字段，用于保存较短的字符串，比如标题
    title = models.CharField(max_length=100)

    # 文章正文。保存大量文本使用 TextField
    body = models.TextField()

    # 文章创建时间。参数 default=timezone.now 指定其在创建数据时将默认写入当前的时间
    created = models.DateTimeField(default=timezone.now)

    # 文章更新时间。参数 auto_now=True 指定每次数据更新时自动写入当前时间
    updated = models.DateTimeField(auto_now=True)
复制代码
```

代码非常直白。**每个模型被表示为 `django.db.models.Model` 类的子类。**每个模型有一些类变量，它们都表示模型里的一个数据库字段。

\**每个字段都是 `Field` 类的实例 。**比如字符字段被表示为 `CharField` ，日期时间字段被表示为 `DateTimeField`。这将告诉 Django 每个字段要处理的数据类型。

\**定义某些 `Field` 类实例需要参数。**例如 `CharField` 需要一个 `max_length`参数。这个参数的用处不止于用来定义数据库结构，也用于验证数据。

\**使用 `ForeignKey`定义一个关系。**这将告诉 Django，每个（或多个） `ArticlePost` 对象都关联到一个 `User` 对象。Django本身具有一个简单完整的账号系统（User），足以满足一般网站的账号申请、建立、权限、群组等基本功能。

`ArticlePost`类定义了一篇文章所必须具备的要素：作者、标题、正文、创建时间以及更新时间。**我们还可以额外再定义一些内容，规范`ArticlePost`中数据的行为。**加入以下代码：

```hljs
article/models.py

...

class ArticlePost(models.Model):
    ...

    # 内部类 class Meta 用于给 model 定义元数据
    class Meta:
    	# ordering 指定模型返回的数据的排列顺序
    	# '-created' 表明数据应该以倒序排列
        ordering = ('-created',)

    # 函数 __str__ 定义当调用对象的 str() 方法时的返回值内容
    def __str__(self):
    	# return self.title 将文章标题返回
        return self.title
复制代码
```

**内部类`Meta`中的`ordering`定义了数据的排列方式。**`-created`表示将以创建时间的倒序排列，保证了最新的文章总是在网页的最上方。**注意`ordering`是元组，括号中只含一个元素时不要忘记末尾的逗号。**

\**`__str__`方法定义了需要表示数据时应该显示的名称。**给模型增加 `__str__`方法是很重要的，它最常见的就是在Django管理后台中做为对象的显示值。因此应该总是返回一个友好易读的字符串。后面会看到它的好处。

整理并去掉注释，全部代码放在一起是这样：

```hljs
article/models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.title
复制代码
```

**恭喜你，你已经完成了博客网站最核心的数据模型的大部分内容。**

代码不到20行，是不是完全没啥感觉。后面会慢慢体会Django的强大。

另外建议新手不要复制粘贴代码。科学表明，缓慢的敲入字符有助于提高编程水平。

## 代码分解

**这部分内容如果不能理解也没关系，先跳过，待水平提高再回过头来阅读。**

### 导入（Import）

Django框架基于python语言，而在python中用`import`或者`from...import`来导入模块。

模块其实就一些函数和类的集合文件，它能实现一些相应的功能。当我们需要使用这些功能的时候，直接把相应的模块导入到我们的程序中就可以使用了。

`import`用于导入整个功能模块。但实际使用时往往只需要用模块中的某一个功能，为此导入整个模块有点大材小用，因此可以用`from a import b`表示从模块`a`中导入`b`给我用就可以了。

### 类（Class）

**Python作为面向对象编程语言，最重要的概念就是类（Class）和实例（Instance）。**

类是抽象的模板，而实例是根据这个类创建出来的一个个具体的“对象”。每个对象都拥有相同的方法，但各自的数据可能不同。而这些方法被打包封装在一起，就组成了类。

比如说我们刚写的这个`ArticlePost`类，作用就是就为博客文章的内容提供了一个模板。每当有一篇新文章生成的时候，都要比对`ArticlePost`类来创建`author`、`title`、`body`...等等数据；虽然每篇文章的具体内容可能不一样，但是必须都遵循相同的规则。

在Django中，数据由模型来处理，而模型的载体就是类（Class）。

### 字段（Field）

字段（field）表示数据库表的一个抽象类，Django使用字段类创建数据库表，并将Python类型映射到数据库。

在模型中，字段被实例化为类属性并表示特定的表，同时具有将字段值映射到数据库的属性及方法。

比方说`ArticlePost`类中有一个`title`的属性，这个属性中保存着`Charfield`类型的数据：即一个较短的字符串。

### ForeignKey外键

**`ForeignKey`是用来解决“一对多”问题的，用于关联查询。**

什么叫“一对多”？

在我们的ArticlePost模型中，**一篇文章只能有一个作者，而一个作者可以有很多篇文章，这就是“一对多”关系**。

又比如一个班级的同学中，每个同学只能有一种性别，而每种性别可以对应很多的同学，这也是“一对多”。

因此，通过`ForeignKey`外键，将`User`和`ArticlePost`关联到了一起，最终就是将博客文章的作者和网站的用户关联在一起了。

既然有“一对多”，当然也有**“一对一”（`OneToOneField`）、“多对多”（`ManyToManyField`）**。目前用不到这些外键，后面再回头来对比其差别。

**注意这里有个小坑，Django2.0 之前的版本`on_delete`参数可以不填；Django2.0以后`on_delete`是必填项，不写会报错。**

### 内部类（Meta）

内部类`class Meta`用来使用类提供的模型元数据。模型元数据是**“任何不是字段的东西”**，例如排序选项`ordering`、数据库表名`db_table`、单数和复数名称`verbose_name`和 `verbose_name_plural`。要不要写内部类是完全可选的，当然有了它可以帮助理解并规范类的行为。

在`class ArticlePost`中我们使用的元数据`ordering = ('-created',)`，表明了每当我需要取出文章列表，作为博客首页时，按照`-created`（即文章创建时间，负号标识倒序）来排列，保证了最新文章永远在最顶部位置。

## 数据迁移（Migrations）

编写好了Model后，接下来就需要进行数据迁移。

迁移是Django对模型所做的更改传递到数据库中的方式。**因此每当对数据库进行了更改（添加、修改、删除等）操作，都需要进行数据迁移。**

Django 的迁移代码是由你的模型文件自动生成的，它本质上只是个历史记录，Django 可以用它来进行数据库的滚动更新，通过这种方式使其能够和当前的模型匹配。

**在虚拟环境中进入`my_blog`文件夹**（还没熟悉venv的再温习: [在Windows中搭建Django的开发环境](https://link.juejin.im/?target=http%3A%2F%2Fwww.dusaiphoto.com%2Farticle%2Farticle-detail%2F4%2F)），输入`python manage.py makemigrations`，**对模型的更改创建新的迁移表**：

```hljs
(env) e:\django_project\my_blog>python manage.py makemigrations
Migrations for 'article':
  article\migrations\0001_initial.py
    - Create model ArticlePost

(env) e:\django_project\my_blog>
复制代码
```

通过运行 `makemigrations` 命令，Django 会检测你对模型文件的修改，并且把修改的部分储存为一次迁移。

然后输入`python manage.py migrate`，**应用迁移到数据库中**：

```hljs
(env) e:\django_project\my_blog>python manage.py migrate
Operations to perform:
  Apply all migrations: admin, article, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
  Applying sessions.0001_initial... OK

(env) e:\django_project\my_blog>
复制代码
```

`migrate` 命令选中所有还没有执行过的迁移并应用在数据库上，也就是将模型的更改同步到数据库结构上。迁移是非常强大的功能，它能让你在开发过程中持续的改变数据库结构而不需要重新删除和创建表。它专注于使数据库平滑升级而不会丢失数据。

有点拗口，如果没懂也没关系，**总之在迁移之后，对Model的编写就算完成了。**