#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Sphantix
# Mail: sphantix@gmail.cn
# created time: Fri 18 May 2018 10:38:09 AM CST
import os
import json
import time
import scrapy


class SmartContractSpider(scrapy.Spider):
    name = "scs"

    def prepare(self):
        local_file = "/home/sphantix/external/code/projects/SmartContract/smart_contract_spider/eth_tokens.json"
        contract_address_list = []
        # 打开本地文件
        with open(local_file, "r") as f:
            file_content = json.loads(f.read())

        # 获取合约地址
        for c in file_content:
            contract_address_list.append(c['address'])

        return contract_address_list

    def write_2_file(self, contract_name, contract_content):
        contract_path = "/home/sphantix/external/code/projects/SmartContract/contracts"

        file_name = "{0}/{1}.sol".format(contract_path, contract_name)
        if os.path.exists(file_name):
            return

        with open(file_name, "w") as f:
            f.write(contract_content)

    def start_requests(self):
        self.log("start_request")
        contract_address_list = self.prepare()
        urls = ["https://etherscan.io/address/{0}#code".format(c) for c in contract_address_list]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        contract_name = str(response.xpath('//*[@id="ContentPlaceHolder1_contractCodeDiv"]/div[2]/table/tr[1]/td[2]/text()').extract_first()).replace("\n", "")
        contract_content = str(response.xpath('//*[@id="editor"]/text()').extract_first())
        self.write_2_file(contract_name, contract_content)
        time.sleep(3)
