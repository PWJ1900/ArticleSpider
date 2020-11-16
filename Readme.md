# 首先看下scrapy学习的几个重要部分（初级学习已完成）

```
Spider
Item
Item loader
Pipeline
Feed export
CrawlSpider
防止被网站禁止：
1、	图片验证码
2、	Ip访问频率限制
3、	User-agent随机切换

Scrapy进阶 – 1、scrapy的原理
            2、基于scrapy的中间件开发
	1、动态网站的抓取处理
	2、将selenuim 和 phantomjs集成到scrapy
	3、scrapy log 配置
	4、email发送
	5、scrapy信号

之后基于scrapy二次开发比如redis-分为几个服务器进行分布式爬虫（这里面集成bloomfilter到scrapy-redis中）
Elasticsearch+django实现一个搜索网站


具体的是:
        数据库：mysql、redis、elasticsearch
        开发环境：virtualenv

一大点：virtualenv和virtualenvwrapper安装和配置
    好处：将我们的开发环境隔离并不影响

使用豆瓣元可以使下载速度加快
-i https://pypi.douban.com/simple/

```

# 具体步骤看docx(下载看) === 从scrapy初步配置开始看


