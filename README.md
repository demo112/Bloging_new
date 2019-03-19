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