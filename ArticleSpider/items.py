# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re

import scrapy

from scrapy.loader.processors import MapCompose, TakeFirst, Identity,Join
from scrapy.loader import ItemLoader


class ArticlespiderItem(scrapy.Item):
  # define the fields for your item here like:
  # name = scrapy.Field()
  pass


# def add_jobbole(value):
#   return value + "-bobby"
#
# def add_jobbole2(value):
#   return value + "-test"


class ArticleItemLoader(ItemLoader):
  default_output_processor = TakeFirst()  # 这都是自带方法里的


def date_convert(value):
  match_re = re.match(".*?(\d+.*)", value)
  if match_re:
    return match_re.group(1)
  else:
    return "1970-07-01"


class JoBoleArticleItem(scrapy.Item):
  title = scrapy.Field(
    # input_processor =  MapCompose(add_jobbole, add_jobbole2)

    # output_processor=TakeFirst()
  )  # 他的所有的字段都是定义的这个类型(可以理解为这里的字段都会逐一的保存放到数据库之中)
  time = scrapy.Field(
    input_processor = MapCompose(date_convert)#此处为自定义的时间获取格式
  )
  url = scrapy.Field()
  url_object_id = scrapy.Field()
  front_image_url = scrapy.Field(
    output_processor=Identity()  # Identity为不受自定义方法影响还是自己的默认类型
  )
  front_image_path = scrapy.Field()
  praise_nums = scrapy.Field()
  comment_nums = scrapy.Field()
  fav_nums = scrapy.Field()
  tags = scrapy.Field(
    output_processor=Join(separator=",")#给tags多个标签加,连接
  )
  content = scrapy.Field()
