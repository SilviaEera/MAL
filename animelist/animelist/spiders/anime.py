# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class AnimeSpider(CrawlSpider):
    name = 'anime'
    allowed_domains = ['myanimelist.net']
    #start_urls = ['https://myanimelist.net/topanime.php/']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://myanimelist.net/topanime.php/', headers={
            'User-Agent': self.user_agent
        })
    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3']/a"), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='link-blue-box next']"))
    )

    def parse_item(self, response):
        yield{
            'Title': response.xpath("//h1[@class='title-name h1_bold_none']/strong/text()").get(),
            'Rating': response.xpath("//div[@class='score-label score-9']/text()").get(),
            'Rank': response.xpath("//span[@class='numbers ranked']/strong/text()").get(),
            'Popularity': response.xpath("//span[@class='numbers popularity']/strong/text()").get(),
            'MAL Members': response.xpath("//span[@class='numbers members']/strong/text()").get(),
            'Season': response.xpath("//span[@class='information season']/a/text()").get(),
            'Aired On': response.xpath("//span[@class='information type']/a/text()").get()
        }
