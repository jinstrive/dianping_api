# Dianping

大众点评网API接口的封装

## Example

* 定义要请求的接口和相应url, 生成DianPingAPI对象调用即可
* 暂只对部分api 进行参数限制

<pre><code>
DPURL = {
    'get_cities_with_businesses': 'http://api.dianping.com/v1/metadata/get_cities_with_businesses',
    'find_businesses': 'http://api.dianping.com/v1/business/find_businesses',
    'get_single_business': 'http://api.dianping.com/v1/business/get_single_business',
    'get_batch_businesses_by_id': 'http://api.dianping.com/v1/business/get_batch_businesses_by_id',
    'get_search_result_url': 'http://api.dianping.com/v1/business/get_search_result_url',
}

from dianping import DingPingAPI

if __name__ == '__main__':
    app_key = 'your app key'
    app_secret = 'your app secret'
    dpapi = DingPingAPI(app_key, app_secret)
    rets = dpapi.find_businesses(city='北京')
    rets = dpapi.find_businesses(city='北京', limit=20)
    ...
</code></pre>


## Contributing

欢迎大家提建议和修改

