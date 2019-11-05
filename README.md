# sofang
此项目作为个人学习爬虫的练手项目，爬取了搜房网的房源信息。

项目需自备代理池。

1.启动
---
  在项目根目录下，使用scrapy crawler sofang.py命令启动。<br/>
  
2.获取代理ip
---
  在middlewares.py中，修改成你自己的代理池的url

```Java
 class ProxyMiddleware(object):
    def process_request(self, request, spider):
        response = requests.get('http://localhost:5010/get')
        while response.status_code != 200:
            response = requests.get('http://localhost:5010/get')

        print('using proxy' + response.json().get('proxy'))
        request.meta['proxy'] = 'http://'+response.json().get('proxy')
```
