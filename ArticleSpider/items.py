# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JoBoleArticleItem(scrapy.Item):
  title = scrapy.Field()#他的所有的字段都是定义的这个类型(可以理解为这里的字段都会逐一的保存放到数据库之中)
  time = scrapy.Field()
  url = scrapy.Field()
  url_object_id = scrapy.Field()
  front_image_url = scrapy.Field()
  front_image_path = scrapy.Field()
  praise_nums = scrapy.Field()
  comment_nums = scrapy.Field()
  fav_nums = scrapy.Field()
  tags = scrapy.Field()
  content = scrapy.Field()

