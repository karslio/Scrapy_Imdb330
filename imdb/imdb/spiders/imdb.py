import scrapy

from ..items import ImdbItem


class FilmSpider(scrapy.Spider):
    name = "films"

    start_urls = [
        "https://www.imdb.com/list/ls004610270/?st_dt=&mode=detail&page=1&ref_=ttls_vm_dtl&sort=list_order,asc"]

    def parse(self, response):
        hrefs = response.css(
            "div.lister-item-content > h3 > a::attr(href)").getall()

        for href in hrefs:
            url = response.urljoin(href)

            yield scrapy.Request(url, callback=self.parse_page)

        next_url = "https://www.imdb.com/" + response.css(
            "a.flat-button.lister-page-next.next-page::attr(href)").get()
        if next_url:
            yield scrapy.Request(url=next_url, callback=self.parse)

    def parse_page(self, response):
        item = ImdbItem()
        film_name = " ".join(response.css(
            "div.title_wrapper > h1::text").get().split())
        date_and_contry = response.css(
            "div.title_wrapper > div > a::text").getall()[-1].split()
        film_date = " ".join(date_and_contry[0:3])
        film_country = date_and_contry[3][1:4]

        film_rate = response.css("div.ratingValue > strong > span::text").get()
        director = response.css(
            "div.plot_summary > div:nth-child(2) > a::text").get()
        stars = response.css(
            " div.plot_summary > div:nth-child(4) > a::text").getall()[0:3]

        item["Film_Name"] = film_name
        item["Film_Date"] = film_date
        item["Film_Country"] = film_country
        item["Film_Rate"] = film_rate
        item["Director"] = director
        item["Stars"] = stars

        yield item
