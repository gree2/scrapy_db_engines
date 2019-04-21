# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from bs4 import BeautifulSoup

from ..items import ScrapyDbEnginesItem
from ..items import ScrapyDbEnginesDbmsItem


class DbenginesSpider(scrapy.Spider):
    name = 'dbengines'
    allowed_domains = ['db-engines.com']
    start_urls = ['https://db-engines.com/en/ranking']

    def parse(self, response):
        # 1.find all ranks
        links = response.xpath('(//div[@class="sidemenu"])[1]//a')
        for link in links:
            # 2.extract rank link
            rank_href = link.xpath('@href').extract()
            rank_text = link.xpath('text()').extract()
            item = ScrapyDbEnginesItem()
            item['rank_href'] = rank_href[0]
            item['rank_text'] = rank_text[0]
            # yield item
            yield Request(
                rank_href[0],
                self.parse_ranking,
                meta={
                    'rank_href': item['rank_href'],
                    'rank_text': item['rank_text']
                }
            )

    def parse_ranking(self, response):
        # 1.find all ranks
        dbmses = response.xpath('//table[@class="dbi"]//tr')
        for dbms in dbmses[3:]:
            # 2.extract rank link
            #  <tr>
            # 1    <td>1.</td>
            # 2    <td class="small">1.</td>
            # 3    <td class="small pad-r">1.</td>
            # 4    <th class="pad-l"><a href="https://db-engines.com/en/system/InterSystems+Cach%C3%A9">InterSystems Caché</a></th> # noqa
            # 5    <th class="small pad-r">Multi-model <span class="info"><img src="https://db-engines.com/info.png"><span class="infobox infobox_r"><b>Key-value store</b>,<br><b>Object oriented DBMS</b>,<br><b>Relational DBMS</b>,<br>Document store</span></span></th> # noqa
            # 6    <td class="pad-l">3.08</td>
            # 7    <td class="small minus">-0.07</td>
            # 8    <td class="small plus">+0.73</td>
            #  </tr>
            item = ScrapyDbEnginesDbmsItem()
            item['rank_href'] = response.meta['rank_href']
            item['rank_text'] = response.meta['rank_text']
            item['rank'] = dbms.css('tr td:nth-child(1)').xpath('text()').extract()[0].replace('.', '') # noqa
            link = dbms.css('tr th:nth-child(4) > a')
            item['name_href'] = link.xpath('@href').extract()
            item['name_text'] = link.xpath('text()').extract()
            item['models'] = self._get_model(dbms)
            yield item

    def _get_model(self, dbms):
        print(dbms.extract())
        model = dbms.css('tr th:nth-child(5)')
        link = dbms.css('tr th:nth-child(5) a')
        span = dbms.css('tr th:nth-child(5) span span')
        if span:
            html = span.extract()[0]
        elif link:
            html = link.extract()[0]
        else:
            html = model.extract()[0]
        models = BeautifulSoup(html, 'html.parser').text
        return models.replace(',', '|')
