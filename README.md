## 新浪微博爬虫
   这个由Python实现的项目可以用来爬取新浪微博的帖子，获取数据由CSV/JSON文件保存！跟其它爬虫相比，这个可能稍微简单点，也是因为我能力不足吧，我还会多多学习，继续改进，还请各位大佬不吝赐教。

请注意，这个项目仅用于学习与交流，如有问题纠纷请不要找我。

## 运行方式
1. 安装依赖
   pip install -r requirements.txt
2. 编辑 src/weibo_spider/main.py
   - 在 settings.keyword 中填入你想爬取的帖子对应的关键词
   - 在 src/weibo_spider/config.py 的 DEFAULT_HEADERS["Cookie"] 填登录 Cookie
3. 运行
   python run.py

## 项目结构

```text
├── .vscode/
│   ├── settings.json
├── original source/    
│   ├── spider_weibo.py  #这是我一开始编辑写的源码
├── output/              #这个文件夹可以存储爬取的文件
├── src/                     
│   ├── __init__.py      
│   ├── client.py        #请求模块
│   ├── config.py        #配置模块
│   ├── crawler.py       #调度模块
│   ├── main.py          #主模块
│   ├── parser.py        #解析模块
│   ├── storage.py       #存储模块
│   └── validators.py    #校验模块                      
├── requirements.text
├── run.py               #运行
└── README.md
```
