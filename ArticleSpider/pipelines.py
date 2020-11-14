# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

import codecs
import json

from scrapy.exporters import JsonItemExporter

import MySQLdb

from twisted.enterprise import adbapi


class ArticlespiderPipeline:
    def process_item(self, item, spider):
        return item

class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
      if "front_image_url" in item:
        image_file_path = ""
        for ok, value in results:
          image_file_path = value["path"]
        item["front_image_path"] = image_file_path

      return item


class JsonWithEncodingPipeline(object):
  #自定义Json文件的导出,这里面方法的名称不能随便写
    def __init__(self):
      self.file = codecs.open("article.json", "a", encoding="utf-8")

    def process_item(self, item, spider):
      lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
      self.file.write(lines)
      return item

    def spider_closed(self, spider):
      self.file.close()


class JsonExporterPipeline(object):
  def __init__(self):
    self.file = open('articleexport.json', 'wb')
    self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
    self.exporter.start_exporting()

  def process_item(self, item, spider):
    self.exporter.export_item(item)
    return item
  def spider_closed(self, spider):
    self.exporter.finish_exporting()
    self.file.close()


class MysqlPipeline(object):
  def __init__(self):
    self.conn = MySQLdb.connect("127.0.0.1", "root", "940731286", "article_spider", charset="utf8", use_unicode=True)
    self.cursor = self.conn.cursor()

  def process_item(self, item, spider):
    insert_sql = """
    insert into jobbole_article(title,url,url_object_id,front_image_url,front_image_path,
    praise_nums,comment_nums,fav_nums,tags,content,time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE praise_nums=(praise_nums)
    """

    params = list()
    # params.append(item["title"])#因为用get会有一个判空的处理步直接加进去少了麻烦
    params.append(item.get("title", ""))
    params.append(item.get("url", ""))
    params.append(item.get("url_object_id", ""))
    front_image = ",".join(item.get("front_image_url", []))
    params.append(front_image)
    params.append(item.get("front_image_path", ""))
    params.append(item.get("praise_nums", 0))
    params.append(item.get("comment_nums", 0))
    params.append(item.get("fav_nums", 0))
    params.append(item.get("tags", ""))
    params.append(item.get("content", ""))
    params.append(item.get("time", "1970-07-01"))
    self.cursor.execute(insert_sql, tuple(params))
    self.conn.commit()
    return item

class MysqlTwistedPipeline(object):
  def __init__(self, dbpool):
    self.dbpool = dbpool
  @classmethod
  def from_settings(cls,setting):
    from MySQLdb.cursors import DictCursor
    dbparms = dict(
      host=setting["MYSQL_HOST"],#这个里面的内容都是再setting里面配置
      db=setting["MYSQL_DBNAME"],
      user=setting["MYSQL_USER"],
      passwd=setting["MYSQL_PASSWORD"],
      charset="utf8",
      cursorclass=DictCursor,
      use_unicode=True,
    )
    dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)#算作一个链接池
    return cls(dbpool) #此处返回给init

  def process_item(self, item, spider):
    query = self.dbpool.runInteraction(self.do_insert, item)#使用下面创建的do_insert方法
    query.addErrback(self.handler_error, item, spider)#也是使用下面的方法

  def handler_error(self, failure, item, spider):
    print(failure)
  def do_insert(self, cursor, item):#cursor是adbapi自动给传递进来的
    insert_sql = """
        insert into jobbole_article(title,url,url_object_id,front_image_url,front_image_path,
        praise_nums,comment_nums,fav_nums,tags,content,time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE praise_nums=(praise_nums)
        """

    params = list()
    # params.append(item["title"])#因为用get会有一个判空的处理步直接加进去少了麻烦
    params.append(item.get("title", ""))
    params.append(item.get("url", ""))
    params.append(item.get("url_object_id", ""))
    front_image = ",".join(item.get("front_image_url", []))
    params.append(front_image)
    params.append(item.get("front_image_path", ""))
    params.append(item.get("praise_nums", 0))
    params.append(item.get("comment_nums", 0))
    params.append(item.get("fav_nums", 0))
    params.append(item.get("tags", ""))
    params.append(item.get("content", ""))
    params.append(item.get("time", "1970-07-01"))
    cursor.execute(insert_sql, tuple(params))






