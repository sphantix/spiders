# SmaCS(Smart Contract Spiders)
主要爬取智能合约, 首先获取智能合约地址, 然后再通过智能合约地址获取智能合约的代码

## 爬取智能合约地址
```shell
$scrapy crawl tas
```

## 爬取智能合约源码
```shell
$scrapy crawl scs
```

## 注意事项
在爬虫代码中, hardcode了一些路径, 请在使用前酌情修改.
