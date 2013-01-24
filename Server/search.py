#coding: utf-8

from Pyzon import pyzon
from pit import Pit
from xml.etree.ElementTree import *

BASE = "{http://webservices.amazon.com/AWSECommerceService/2011-08-01}"

def parse_result_xml(xml):
    result = [];

    root = fromstring(xml);
    items = root.findall(".//" + BASE + "Item");
    for item in items:
        url = filter(lambda (x):x.tag == BASE + "DetailPageURL", list(item))[0].text;
        try:
            image = item.find(".//%sMediumImage" % BASE).findtext(".//%sURL" % BASE);
        except:
            image = "";
        title = item.find(".//%sTitle" % BASE);
        id = item.find(".//%sASIN" % BASE).text;
        try:
            author = item.find(".//%sAuthor" % BASE).text;
        except AttributeError:
            author = "";

        result.append({
            "_id": id,
            "url": url,
            "image": image,
            "title": title.text,
            "author": author,
        });
    return result;

def amazon_search(page, title=None, author=None, keyword=None):
    amazon = Pit.get("amazon");
    api = pyzon.Pyzon(amazon["key"], amazon["secret"], "pinkroot-22");
    if title:
        xml = api.ItemSearch("Books", Title=title, ItemPage=str(page), ResponseGroup="Images,ItemAttributes");
    if author:
        xml = api.ItemSearch("Books", Author=author, ItemPage=str(page), ResponseGroup="Images,ItemAttributes");
    if keyword:
        xml = api.ItemSearch("Books", Keywords=keyword, ItemPage=str(page), ResponseGroup="Images,ItemAttributes");
    result = parse_result_xml(xml);
    return result;

if __name__ == "__main__":
    print amazon_search(1, author=u"西尾");

