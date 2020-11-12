import json
import re
from urllib import parse#此方法使用url加入

import requests
import scrapy#scrapy是异步io框架 没有多线程，没有引入消息队列
from scrapy import Request


from ArticleSpider.utils import common
from ArticleSpider.items import JoBoleArticleItem

class JobboleSpider(scrapy.Spider):
  name = 'jobbole'
  allowed_domains = ['news.cnblogs.com']
  start_urls = ['http://news.cnblogs.com/']

  def parse(self, response):
    """
    1、获取新闻列表页中的行文url并交给scrapy进行下载后调用相应的解析方法
    2、获取下一页的url并交给scrapy进行下载，下载完成后交给parse继续跟进
    :param response:
    :return:
    # """
    post_nodes = response.css("#news_list .news_block")[:1]
    for post_node in post_nodes:
      image_url = post_node.css(".entry_summary a img::attr(href)").extract_first("")#获取图片
      post_url = post_nodes.css("h2 a::attr(href)").extract_first("")#获取标题链接
      yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)#这里面的parse可以解决重复添加url的问题,记住方法加括号就是一个返回值了

      #下一页的提取 这边分别用css和xpath进行操作如果用的xpath函数可以不用if判断
    #Way1
    # next_url = response.css("div.pager a:last-child::text").extract_first("")
    # if next_url == "Next >":
    #   next_url = response.css("div.pager a:last-child::attr(href)").extract_first("")
    #   yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    #Way2
    # next_url = response.xpath("//a[contains(text(),'Next >')]/@href").extract_first("")
    # yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)



  def parse_detail(self, response):
    match_re =re.match(".*?(\d+)", response.url)#先判断url有没有id
    if match_re:
      post_id = match_re.group(1)  # 此处提取post_id来给下面的的id赋值

      article_Item = JoBoleArticleItem()


      title = response.css("#news_title a::text").extract_first("")
      time = response.css("#news_info .time::text").extract_first("")
      match_re = re.match(".*?(\d+.*)", time)
      if match_re:
        time = match_re.group(1)
      content = response.css("#news_content").extract()[0]
      tag_list = response.css(".news_tags a::text").extract()

      # title = response.xpath("//*[@id='news_title']//a/text()").extract_first("")
      # time = response.xpath("//*[@id='news_info']//*[@class='time']/text()").extract_first("")
      # content = response.xpath("//*[@id='news_content']").extract()[0]
      # tag_list = response.xpath("//*[@class='news_tags']//a/text()").extract()
      tags = ",".join(tag_list)



      # html = requests.get(parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)))#注意因为requests是同步的而这里用的是一个异步的方法，所以换异步的方法实现,    得加/
      # j_data = json.loads(html.text)

      article_Item["title"] = title#这里面一定要确保key是在item里面存在的
      article_Item["time"] = time
      article_Item["tags"] = tags
      article_Item["content"] = content
      article_Item["url"] = response.url
      article_Item["front_image_url"] = response.meta.get("front_image_url","")#可以通过此方法获得传递过来的图片值

      #用yeid把上方法换成异步
      yield Request(url=parse.urljoin(response.url, "/NewsAjax/GetAjaxNewsInfo?contentId={}".format(post_id)),
                    meta={"article_item": article_Item}, callback=self.parse_nums)

  def parse_nums(self, response):
    article_item = response.meta.get("article_item", "")
    j_data = json.loads(response.text)
    praise_nums = j_data["DiggCount"]
    fav_nums = j_data["TotalView"]
    comment_nums = j_data["CommentCount"]

    article_item["praise_nums"] = praise_nums
    article_item["fav_nums"] = fav_nums
    article_item["comment_nums"] = comment_nums
    article_item["url_object_id"] = common.get_md5(article_item["url"])

    yield article_item


