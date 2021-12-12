# Python Spider Demo

## novel_spider

爬取 [笔趣看](https://www.bqktxt.com/) 网站的小说

## picture_spider

爬取 [Unsplash](https://unsplash.com/) 网站的图片

> 初次运行前需要在项目根目录下新建`images`文件夹。

## weibo_hot_spider

爬取微博热搜数据
> 请求需要带上`cookie`

- 使用的MySQL
- 创建数据库 `weibo_hot`
- PyCharm 连接MySQL报错

  `No appropriate protocol (protocol is disabled or cipher suites are inappropriate`

  解决方案：在URL中添加 `?createDatabaseIfNotExist=true&useSSL=false`

  如： `jdbc:mysql://192.168.2.2:3306/test?createDatabaseIfNotExist=true&useSSL=false`

- python 连接mysql报错

  `[SSL: UNSUPPORTED_PROTOCOL]`

  解决方案：关闭mysql的ssl

  1. 查看当前的mysql有没有启动ssl（`show variables like '%ssl%';`）
  2. 在/etc/mysql/my.cnf文件文件中的 [mysqld] 段添加 skip-ssl 表示跳过ssl
  3. 重启mysql，再查看是否关闭了ssl

  > 创建数据库时可添加 `--skip-ssl` 来禁用ssl。