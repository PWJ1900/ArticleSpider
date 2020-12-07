
import scrapy  # scrapy是异步io框架 没有多线程，没有引入消息队列

from selenium import webdriver
import time

from mouse import move,click

import pickle

class JobboleSpider(scrapy.Spider):
  name = 'zhihu'
  allowed_domains = ['www.zhihu.com']
  start_urls = ['https://www.zhihu.com/']



  def parse(self, response):
    pass



  def start_requests(self):
    # 此方式手动去启动chrome

    # 使用自己手动启动的实例
    # from selenium.webdriver.chrome.options import Options
    #
    # chrome_options = Options()
    # chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")#指定使用手动打开的端口
    #
    #
    # browser = webdriver.Chrome(executable_path="H:/ArticleSpider/ArticleSpider/utils/chromedriver.exe", chrome_options=chrome_options)


    cookies = pickle.load(open("cookies/zhihu.cookie", 'rb'))#前面获取了cookie后续直接用它就行了，其他前面获取的逻辑就不用用了
    cookie_dic = {}
    for cookie in cookies:
      cookie_dic[cookie["name"]] = cookie['value']

    return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dic)]

    # browser.find_element_by_css_selector('.SignFlow-tabs div:nth-child(2)').click()
    # browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper .Input').send_keys('17706273627')
    # browser.find_element_by_css_selector('.SignFlow-password .Input').send_keys('18752719-p')
    #
    #
    # time.sleep(3)
    # # 使用move定位
    # move(765, 494)
    # click()
    #
    # # browser.find_element_by_css_selector('button[type="submit"]').click()
    # time.sleep(60)

#     browser.get('https://www.zhihu.com/signin')
#     cookies = browser.get_cookies()
# #     这里面使用cookies来序列化包
#     pickle.dump(cookies, open("cookies/zhihu.cookie", "wb"))#可以直接把对象放到文件当中
#     cookie_dic = {}
#     for cookie in cookies:
#       cookie_dic[cookie["name"]] = cookie['value']
#
#     return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dic)]




