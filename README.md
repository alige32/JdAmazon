因为京东反爬比较严格，但ip情况下多线程都不敢开

方案：requests请求页面配合xpath做页面解析，因为京东页面是前后端分离，返回来的是网页结构。我们需要的价格等动态数据在JS脚本文件里边（有的网站会在XHR，即json数据），这都需要我们审查元素在network里边抓包查看

请求url地址，range里边是页面范围，可根据需求修改

```
self.urls = [
            'https://list.jd.com/list.html?cat=1713,3287,3804&page={}&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main'.format(
                i) for i in range(0, 1)]
```
动态数据接口。{}里边为商品id，通过xpath提取商品对应链接，再通过正则匹配提取id，拼接url

```
self.price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{}&pduid=1529748008301614117965'
```
请求回来的是js对象的字符串而非json数据！！！


```
[
{
op: "46.60",
m: "59.00",id: "J_11962552",
p: "46.60"
}
]
```
通过

```
price = eval(js_str)[0]['p']
```

本次提取了4个字段，可根据需求增加提取。用pandas读取查看，后边继续更新数据分析

```
import pandas as pd
import numpy as np


datas=pd.read_json('jd.json',orient="records", lines=True)
datas
```
![jddatas]($res/jddatas.png)

