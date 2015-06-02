# -*- coding: utf-8 -*-
import types
import hashlib
import requests
from urllib import urlencode
from functools import partial

TIMEOUT = 5

class DianPingAPI(object):

    def __init__(self, app_key, app_secret):
        self.app_key = app_key
        self.app_secret = app_secret

    def request_url(self, attr, **kwargs):
        """
        请求基础方法
        :param attr:
        :param kwargs:
        :return:
        """
        url = DPURL.get(attr, '')
        assert url
        r_url = '%s?%s' % (
            url,
            request_param_with_sign(kwargs, self.app_key, self.app_secret)
        )
        print r_url
        rq = requests.get(r_url, timeout=TIMEOUT)
        if kwargs.get('format', 'json') == 'json':
            return rq.json()
        else:
            return rq.text

    def get_cities_with_businesses(self, **kwargs):
        """
        获取城市
        return: {"status":"OK","cities":["全国","上海","北京","杭州",...]}
        """
        if not kwargs:
            kwargs = {}
        return self.request_url('get_cities_with_businesses', **kwargs)

    def find_businesses(self, **kwargs):
        """
        搜索商户
        返回值如下
        {
        "status": "OK",
        "total_count": 40,
        "businesses": [
            {
                "coupon_url": "",
                "rating_img_url": "http://i3.dpfile.com/s/i/app/api/32_0star.png",
                "avg_price": 0,
                "telephone": "4006040616",
                "coupon_id": 0,
                "product_grade": 0,
                "rating_s_img_url": "http://i3.dpfile.com/s/i/app/api/16_0star.png",
                "online_reservation_url": "",
                "has_coupon": 0,
                "business_url": "http://www.dianping.com/shop/1916992?utm_source=open",
                "city": "北京",
                "review_count": 0,
                "product_score": 0,
                "regions": [
                    "朝阳区",
                    "十八里店"
                ],
                "review_list_url": "http://www.dianping.com/shop/1916992/review_all?utm_source=open",
                "s_photo_url": "http://i3.dpfile.com/pc/b099c99ef4c018d45f851ce193bf1cbb(278x200)/thumb.jpg",
                "latitude": 39.868042,
                "decoration_grade": 0,
                "photo_count": 4971,
                "service_grade": 0,
                "has_online_reservation": 0,
                "business_id": 1916992,
                "branch_name": "",
                "decoration_score": 0,
                "service_score": 0,
                "has_deal": 1,
                "categories": [
                    "游乐场"
                ],
                "photo_url": "http://i1.dpfile.com/pc/b099c99ef4c018d45f851ce193bf1cbb(700x700)/thumb.jpg",
                "distance": -1,
                "name": "北京欢乐谷(这是一条测试商户数据，仅用于测试开发，开发完成后请申请正式数据...)",
                "coupon_description": "",
                "avg_rating": 0,
                "longitude": 116.494255,
                "deals": [
                    {
                        "url": "http://dpurl.cn/p/e624gyqg0c",
                        "id": "2-2279359",
                        "description": "北京欢乐谷直通车!仅售178元，价值258元北京欢乐谷直通车，无强制消费，每日发团！"
                    },
                ],
                "photo_list_url": "http://www.dianping.com/shop/1916992/photos?utm_source=open",
                "deal_count": 18,
                "address": "朝阳区东四环南路东侧小武基路路北(四方桥东南角)"
            }
        ],
        "count": 40,
        }
        """
        if not kwargs or not isinstance(kwargs, dict):
            raise ValueError
        if 'latitude' in kwargs and 'longitude' not in kwargs:
            raise AssertionError
        if 'city' in kwargs and 'latitude' in kwargs:
            raise AssertionError
        if 'limit' not in kwargs:
            kwargs.update({'limit': 40})
        return self.request_url('find_businesses', **kwargs)

    def get_single_business(self, business_id, out_offset_type=1, platform=1, f='json'):
        """
        获取指定商户信息 Business/get_single_business
        :param business_id int: 商户ID
        :param out_offset_type int: 传出经纬度偏移类型，1:高德坐标系偏移，2:图吧坐标系偏移，如不传入，默认值为1
        :param platform int: 传出链接类型，1:web站链接（适用于网页应用），2:HTML5站链接（适用于移动应用和联网车载应用），如不传入，默认值为1
        :param format string: 返回数据格式，可选值为json或xml，如不传入，默认值为json

        返回值  同搜索商户
        """
        return self.request_url('get_single_business',
                                business_id=business_id,
                                out_offset_type=out_offset_type,
                                platform=platform,
                                format=f)

    def get_batch_businesses_by_id(self, business_ids, out_offset_type=1, platform=1, f='json'):
        """
        批量获取指定商户信息 business/get_batch_businesses_by_id
        :param business_id int: 一个或多个商户ID集合，多ID之间以英文逗号分隔，如“4659232,5257123,5185318”，一次传入的ID数量上限为40个，其他参数限制请参考下方注意事项
        :param out_offset_type int: 同上方法
        :param platform int: 同上方法
        :param format string: 同上方法

        返回值  同搜索商户
        """
        return self.request_url('get_batch_businesses_by_id',
                                business_id=business_ids,
                                out_offset_type=out_offset_type,
                                platform=platform,
                                format=f)

    def get_search_result_url(self, city, **kwargs):
        """
        获取指定结果列表页面链接 business/get_search_result_url
        必须参数
        city 城市名称，可选范围见相关API返回结果
        可选参数：
        region string 城市区域名，可选范围见相关API返回结果（不含返回结果中包括的城市名称信息）
        category string 分类名，可选范围见相关API返回结果;支持多个category搜索，最多5个
        keyword string 关键词，搜索范围包括商户名、地址、标签等
        sort int 结果排序，1:默认，2:星级高优先，3:产品评价高优先，4:环境评价高优先，5:服务评价高优先，6:点评数量多优先
        platform int 传出链接类型，1:web站链接（适用于网页应用），2:HTML5站链接（适用于移动应用和联网车载应用），如不传入，默认值为1
        format string 返回数据格式，可选值为json或xml，如不传入，默认值为json
        """
        if not city or not isinstance(city, basestring):
            raise AssertionError
        kwargs.update({'city': city})
        return self.request_url('get_search_result_url', **kwargs)

    def __getattr__(self, item):
        """
        支持动态获取不同请求
        """
        return partial(self.request_url, attr=item)



def request_param_with_sign(param_dict, app_key, app_secret):
    """
    请求参数 添加sign
    :param param_dict:
    :param app_key:
    :param app_secret:
    :return:
    """
    if 'appkey' in param_dict:
        param_dict.pop('appkey')
    parsort = sorted(param_dict.iteritems(), key=lambda d: d[0], reverse=False)
    parstr = '{app_key}{paramstr}{app_secret}'.format(
        app_key=app_key,
        paramstr=''.join([''.join((str(k), unicode2utf8(str(v)))) for k, v in parsort]),
        app_secret=app_secret,
    )
    sign = hashlib.sha1(parstr).hexdigest().upper()
    param_dict.update({'sign': sign, 'appkey': app_key})
    return urlencode(param_dict)


def unicode2utf8(text):
    """
    unicode to utf8
    :param text:
    :return:
    """
    if isinstance(text, types.UnicodeType):
        return text.encode('utf-8')
    else:
        return text


# 点评各请求的url
DPURL = {
    'get_cities_with_businesses': 'http://api.dianping.com/v1/metadata/get_cities_with_businesses',
    'find_businesses': 'http://api.dianping.com/v1/business/find_businesses',
    'get_single_business': 'http://api.dianping.com/v1/business/get_single_business',
    'get_batch_businesses_by_id': 'http://api.dianping.com/v1/business/get_batch_businesses_by_id',
    'get_search_result_url': 'http://api.dianping.com/v1/business/get_search_result_url',
}


def test_api():
    app_key = 'your app key'
    app_secret = 'your app secret'
    dpapi = DianPingAPI(app_key, app_secret)
    dpapi.get_cities_with_businesses()
    dpapi.find_businesses(city='北京', page=4, limit=40)


if __name__ == '__main__':
    app_key = '32031532'
    app_secret = 'f9f6707d865047d19bd1006f36628a37'
    dpapi = DianPingAPI(app_key, app_secret)
    # dpapi.get_cities_with_businesses()
    rets = dpapi.find_businesses(city='北京', limit=20, page=7)
    print rets
