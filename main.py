from scrapy.cmdline import execute
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))#将当前路径
# execute(["scrapy", "crawl", "jobbole"])
execute(["scrapy", "crawl", "zhihu"])
