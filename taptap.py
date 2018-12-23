#!usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import urllib3
from lxml import etree
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TapTap(object):
    def __init__(self):
        # self.start_url = ["https://www.taptap.com/top/download",
        #                   "https://www.taptap.com/top/reserve",
        #                   "https://www.taptap.com/top/sell",
        #                   "https://www.taptap.com/top/played"]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit"
                          "/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
        }
        self.next_url = ["https://www.taptap.com/ajax/top/download?page={page}&total=0",
                         "https://www.taptap.com/ajax/top/reserve?page={page}&total=0",
                         "https://www.taptap.com/ajax/top/played?page={page}&total=0"]

    def parse_url(self, url, page):
        response_add = requests.get(url.format(page=page), headers=self.headers, verify=False)
        html = response_add.json()
        return html

    def get_game_list(self, html_content):
        html_str = etree.HTML(html_content['data']['html'])
        container = html_str.xpath("//div[@class='taptap-top-card']")
        game_list = list()
        for content in container:
            item = dict()
            item['name'] = content.xpath("./div/a/img/@title")[0]
            item['href'] = content.xpath("./div/a/@href")[0]
            item['score'] = content.xpath("./div[3]/p/text()")[0].strip()
            game_list.append(item)
        return game_list

    def run(self):
        games_list = list()
        for i in range(len(self.next_url)):
            for j in range(1, 6):
                html_content = self.parse_url(self.next_url[i], j)
                games = self.get_game_list(html_content)
                for game in games:
                    games_list.append(game)
        with open("game.json", "w", encoding="utf-8") as f:
            f.write(json.dumps(games_list, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    tap = TapTap()
    tap.run()
