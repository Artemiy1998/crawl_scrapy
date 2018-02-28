from megapol.items import MegapolItem
import scrapy
from urllib.parse import urljoin


class MegapolSpider(scrapy.Spider):
    name = "megapol"
    url_name = 'https://www.megapolisonline.ru'
    start_urls = [
        'https://www.megapolisonline.ru/?limit=10&page=1',
    ]

    def parse(self, response):
        date_user = ['27', 2, '2018']
        for post_item in response.css('div.post-item'):
            date = post_item.css('div.date-time::text').extract_first()
            date_list = date.split()
            date_list.pop()
            date_list[1] = self.month_convert(date_list[1])
            if all([(date_list[0] == date_user[0]), (date_list[1] == date_user[1]), (date_list[2] == date_user[2])]):
                yield response.follow(
                    response.urljoin(post_item.css('a.image::attr(href)').extract_first()), callback=self.parse_post,encoding='utf=8')
            elif date_list[0] < date_user[0]:
                quit()
            elif date_list[0] > date_user[0] and date_list[1] < date_user[1]:
                quit()

        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

    def month_convert(self, month):
        month_dict = {'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4, 'мая': 5, 'июля': 6, 'июня': 7, 'августа': 8,
                      'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12}
        if month in month_dict:
            month_int = month_dict[month]
        return month_int

    def parse_post(self, response):
        item = MegapolItem()
        url_post = response.url
        item['url_post'] = url_post
        body = response.css('div.post-message::text').extract()
        item['body'] = body
        date = response.css('div.date-time::text').extract_first()
        item['date'] = date
        yield item
