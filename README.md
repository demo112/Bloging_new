# 数据库备份

## 完整数据库备份与恢复

```python
    # 备份
    python manage.py dumpdata > mysite_all_data.json
    # 恢复
    python manage.py loaddata mysite_all_data.json
```

## 单独表备份与恢复

```python
    # 备份
    python manage.py dumpdata [appname] > appname_data.json
    # 示例
    python manage.py dumpdata blog > blog_dump.json
    python manage.py dumpdata auth > auth.json # 导出用户数据
    # 恢复
    python manage.py loaddata blog_dump.json
```

# 虚拟环境

## 工具

### pipenv

#### 安装

```cmd
$ brew install pipenv
or
$ sudo dnf install pipenv
or
$ pip install --user pipenv
```

#### 使用

要初始化Python 3虚拟环境，请运行 `$ pipenv --three`

要初始化Python 2虚拟环境，请运行`$ pipenv --two`

###### 找到项目

```cmd
$ pipenv --where
```

###### 找到virtualenv

```cmd
$ pipenv --venv
```

###### 找到Python解释器

```cmd
$ pipenv --py
```

###### 安装包

```cmd
$ pipenv install packge_name
```

###### 生成一个锁文件

```cmd
$ pipenv lock
```

###### 卸载一切

```cmd
$ pipenv uninstall --all
```

### Git

```cmd
   add        Add file contents to the index
   bisect     Find by binary search the change that introduced a bug
   branch     List, create, or delete branches
   checkout   Checkout a branch or paths to the working tree
   clone      Clone a repository into a new directory
   commit     Record changes to the repository
   diff       Show changes between commits, commit and working tree, etc
   fetch      Download objects and refs from another repository
   grep       Print lines matching a pattern
   init       Create an empty Git repository or reinitialize an existing one
   log        Show commit logs
   merge      Join two or more development histories together
   mv         Move or rename a file, a directory, or a symlink
   pull       Fetch from and merge with another repository or a local branch
   push       Update remote refs along with associated objects
   rebase     Forward-port local commits to the updated upstream head
   reset      Reset current HEAD to the specified state
   rm         Remove files from the working tree and from the index
   show       Show various types of objects
   status     Show the working tree status
   tag        Create, list, delete or verify a tag object signed with GPG
```



# 项目依赖包

***pip install Pillow django==2.1.7 markdown pygments django-password-reset***

# 运行项目

```cmd
git init
cd
cd https\:/
git clone https://github.com/demo112/Bloging_new.git
cd Bloging_new/
python3 manage.py runserver 0.0.0.0:8000
```

