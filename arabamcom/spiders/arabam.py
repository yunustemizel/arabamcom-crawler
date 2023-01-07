import scrapy
import re
import json

class ArabamSpider(scrapy.Spider):
    name = 'arabam'
    allowed_domains = ['arabam.com']
    start_urls = ['https://www.arabam.com/ikinci-el']
    items=[]
    def parse(self, response):
    
        listing = response.xpath('//a[@class="link-overlay"]/@href').getall()

        for detail in listing:
            yield scrapy.Request(url="https://www.arabam.com" + detail, callback=self.parseItems)
   
        try:
            nextPage =response.xpath('//a[@id="pagingNext"]/@href').get()
            yield scrapy.Request(url="https://www.arabam.com"+nextPage, callback=self.parse)
        except:
            jsonString = json.dumps(self.items,ensure_ascii=False)
            jsonFile = open("data.json", "w",encoding='utf8')
            jsonFile.write(jsonString)
            jsonFile.close()
                         
    def parseItems(self, response):
        data = {
            "title": response.xpath('//p[@class="advert-detail-title"]/text()').get(""),
            "price": re.findall(r'"Price":(.*?),"', response.text),
            "make": response.xpath('//span[contains(text(),"Marka:")]/following-sibling::span/text()').get("").strip(),
            "model": response.xpath('//span[contains(text(),"Model:")]/following-sibling::span/text()').get("").strip(),
            "pictures": response.xpath('//a[@class="slick-wrapper"]/img/@data-src-sophisticated').getall(),
            "year": response.xpath('//span[contains(text(),"Yıl:")]/following-sibling::span/text()').get("").strip(),
            "mileage": response.xpath('//span[contains(text(),"Kilometre:")]/following-sibling::span/text()').get("").strip(),
            "transmissionType": response.xpath('//span[contains(text(),"Vites Tipi:")]/following-sibling::span/text()').get("").strip(),
            "fuelType": response.xpath('//span[contains(text(),"Yakıt Tipi:")]/following-sibling::span/text()').get("").strip(),
            "bodyType": response.xpath('//span[contains(text(),"Kasa Tipi:")]/following-sibling::span/text()').get("").strip(),
            "engineSize": response.xpath('//span[contains(text(),"Motor Hacmi:")]/following-sibling::span/text()').get("").strip()
        }
        
        self.items.append(data)
        
        