# coding = utf-8
from Util import Util


def get_China_top500():
    base_url = "http://www.fortunechina.com/search/f500beta/search.do?facetAction=&facetStr=type%23%E6%89%80%E5%B1%9E%E6%A6%9C%E5%8D%95%23%E4%B8%AD%E5%9B%BD500%E5%BC%BA%3B&sort=1&key=&curPage="
    host = "www.fortunechina.com"
    header = Util.get_header(host)
