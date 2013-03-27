# 什么是ScriptFan.com

[ScriptFan.com](http://scriptfan.com) 是西安一个线下技术沙龙的官方网站程序, 沙龙的名字是**ScriptFan技术沙龙**, 
主要以讨论脚本语言为主, 比如 Python, Perl, PHP, Ruby, Shell, JavaScript, CoffeeScript 等.

## 网站主要功能

 1. 发布活动和新闻
 2. 用户名片
 3. 用户讨论
 4. 每期线下活动的话题的总结

## 网站程序简介

网站使用 Python 语言写成, 用到了 Flask 作为主要框架, SqlAlchemy 作为 ORM 框架，页面效果使用的是 Bootstrap。

## 贡献代码，从这里开始

> 欢迎熟悉 Python, Flask, SqlAlchemy 的朋友一起参与开发 ，数据库的 Migration 工具采用 SqlAlchemy 作者开发的 
> [alembic](http://alembic.readthedocs.org/en/latest/tutorial.html#editing-the-ini-file), 
> 方便在开发过程中持续的改进数据库结构, 有兴趣参与开发的同学需要先学习下.
> 申请开发权限，请联系 david.scriptfan#gmail.com

### 1. 下载项目并安装依赖库

    $ git@github.com:kingheaven/ScriptFan.com.git
    $ cd ScriptFan.com
    $ git checkout -b dev origin/dev
	$ virtualenv venv
	$ . venv/bin/activate
    (venv) $ pip install -v -r requirements.txt

### 2. 数据库配置

在本地数据库中建立一个数据库，如 `scriptfan_dev`

**注意：** 请确保数据库、表及字段的 Collation 为 utf8 `utf8_unicode_ci` 类型

修改配置文件

    $ cp website/scriptfan/scriptfan.cfg.sample website/scriptfan/scriptfan.cfg
    $ cp website/alembic.ini.sample website/alembic.ini

将 `website/scriptfan/scriptfan.cfg` 中的 `SQLALCHEMY_DATABASE_URI` 及 `website/alembic.ini` 中的 `sqlalchemy.url` 替换为你的数据库配置

### 3. 更新数据库结构

    $ cd website
    $ alembic upgrade head

### 4. 启动本地开发服务器

    $ python manager.py runserver

### 5. 更新i18n语言文件

在 `website/scriptfan` 目录下执行

    $ python manage.py translate

