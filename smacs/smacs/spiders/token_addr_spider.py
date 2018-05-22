#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Author: Sphantix
# Mail: sphantix@gmail.cn
# created time: Fri 18 May 2018 10:38:09 AM CST
import json
import time
import scrapy
import threading


class TokenAddressSpider(scrapy.Spider):
    name = "tas"
    address_set = set()

    def write_2_file(self, address_set):
        contract_path = "/home/sphantix/external/code/projects/SmartContract/smart_contract_spider"
        with open("{0}/eth_tokens.json".format(contract_path), "r+") as f:
            content = json.load(f)

            for address in address_set:
                content.append({"address": address})

            f.truncate()
            json.dump(content, f, indent=4)

    def start_requests(self):
        urls = ["https://etherscan.io/tokens?p={0}".format(c) for c in range(1, 11)]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        token_addresses = response.css('a::attr(href)').re('0x[0-9a-fA-F]+')

        for address in token_addresses:
            self.address_set.add(str(address))

        if len(self.address_set) > 460:
            self.write_2_file(self.address_set)
        time.sleep(3)
