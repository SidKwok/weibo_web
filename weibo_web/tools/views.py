# coding:utf-8
__author__ = 'Sid'
from django.http import HttpResponse
from django.shortcuts import render
from lxml import etree
import urllib2
import json

# 导入包装的csrf请求，对跨站攻击脚本做处理
from django.views.decorators.csrf import csrf_exempt

try:
    from django.http import JsonResponse
except ImportError:
    from .tool import JsonResponse

me = {"name":"sid","sex":"男","area":"广东","url":"1","icon":"http://tp1.sinaimg.cn/2864830740/180/5692138077/1"}

def index(request):
    return render(request, 'index.html')

# 获取资料
@csrf_exempt
def search(request):
    selector = getPage("/nickname?page=1&vt=4")
    profile = getInfo(selector)
    print profile['name']
    print profile['sex']
    print profile['area']
    # print profile['birthday']
    # print profile['summary']

    return HttpResponse(json.dumps(profile))

# 获取粉丝
@csrf_exempt
def fansearch(request):
    t_url = "/nickname?page=1&vt=4"
    selector = getPage(t_url)
    fansList = []
    # 将个人信息添加进去
    profile = getInfo(selector)
    profile['url'] = "http://weibo.com" + t_url
    fansList.append(profile);
    selec = getFansPage(selector)
    getFans(selec, fansList)

    # for test
    # fansList1 = []
    # fansList1.append({"name":"sid","sex":"男","area":"广东","url":"http://weibo.com/sidkwok","icon":"http://tp1.sinaimg.cn/2864830740/180/5692138077/1"})
    # fansList1.append({"name":"natalie","sex":"女","area":"广东","url":"http://weibo.com/natalie9478","icon":"http://tp4.sinaimg.cn/1771999403/180/5736406177/0"})
    # fansList1.append({"name":"mingen","sex":"女","area":"广东","url":"http://weibo.com/whiterosez","icon":"http://tp3.sinaimg.cn/1745779710/180/5739175356/0"})
    # fansList1.append({"name":"cici","sex":"n女","area":"湖北","url":"http://weibo.com/yansiqi147","icon":"http://tp4.sinaimg.cn/2473635775/180/5724097749/0"})
    # fansList1.append({"name":"airdy","sex":"女","area":"美国","url":"5","icon":"http://tp3.sinaimg.cn/5704726886/180/5737511626/0"})
    return HttpResponse(json.dumps(fansList))


def packHeader(url):
    HEADER = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0",
        "Cookie":"yourcookie"
    }
    req = urllib2.Request(url,headers=HEADER)
    r = urllib2.urlopen(req)
    html = r.read()
    selector = etree.HTML(html)
    return selector

# 发送带Cookie的消息头并获取页面之后用selector进行定义
def getPage(page):
    url = "http://weibo.cn" + page
    selector = packHeader(url)
    return selector

# 获取资料
def getInfo(selector):
    profile = dict()
    m_url = selector.xpath('//*[@class="ut"]/a[2]/@href')
    profile_url = "http://weibo.cn" + m_url[0]
    selec = packHeader(profile_url)
    p = selec.xpath('/html/body/div[@class="c"][3]/text()')
    profile['name'] = p[0][3:].encode('utf-8')
    profile['sex'] = p[1][3:].encode('utf-8')
    profile['area'] = p[2][3:].encode('utf-8')
    profile['icon'] = selec.xpath('//*[@class="c"][1]/img/@src')[0]
    # profile['birthday'] = p[3][3:].encode('utf-8')
    # profile['summary'] = p[4][3:].encode('utf-8')

    return profile

# 获取粉丝
def getFansPage(selector):
    m_url = selector.xpath('//*[@class="tip2"]/a[2]/@href')
    fans_url = "http://weibo.cn" + m_url[0]
    selec = packHeader(fans_url)
    return selec

def getFans(selector,fansList):
    # 创建粉丝个人信息字典
    fan = dict()

    fans = selector.xpath('//div[@class="c"]/table/tr/td[2]/a[1]')
    fans_url = selector.xpath("//table/tr/td[1]/a/@href")
    # print fans
    next_url = selector.xpath('//*[@id="pagelist"]/form/div/a[1]/@href')
    next_data = selector.xpath('//*[@id="pagelist"]/form/div/a[1]/text()')

    for each_fan, each_url in zip(fans,fans_url):
        # fan = each.xpath('string(.)').encode('utf-8')
        if (each_fan.xpath('string(.)').encode('utf-8')=='hs_GXocean'):
            fansList.append(me)

        else:
            # 获取粉丝资料
            fan = getInfo(getPage(each_url[15:]))
            fan['url'] = "http://weibo.com"+each_url[15:]

            fansList.append(fan)
            # print fan
            print fan['name']
            print fan['sex']
            print fan['area']
            print fan['url']
            print fan['icon']

    # 判断是否爬取到最后一页
    if next_data[0] == u'\u4e0a\u9875':
        return 0
    selec = getPage(next_url[0])
    getFans(selec,fansList)
