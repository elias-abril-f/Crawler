import scrapy


class SpiderrightmoveSpider(scrapy.Spider):
    name = 'spiderRightMove'
    allowed_domains = ['rightmove.co.uk']

    def __str__ (self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(SpiderrightmoveSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        for i in range(0, 24*42, 24):
            yield scrapy.Request(f"https://www.rightmove.co.uk/property-to-rent/find.html?searchType=RENT&locationIdentifier=OUTCODE^{self.search_code}&insId=1&radius={self.radius}&maxBedrooms={self.max_beds}&minBedrooms={self.min_beds}&maxPrice={self.max_price}&minPrice={self.min_price}&index={i}&propertyTypes=&maxDaysSinceAdded=14&includeLetAgreed=false&mustHave=&dontShow=&furnishTypes=&keywords=")


    def parse(self, response):
        
        listings = response.xpath('//*[@id="l-searchResults"]/div')
        
        URL = "https://www.rightmove.co.uk"
        
        for listing in listings:
            
            try:
                # Manipulate the data to clean the data and divide one query into multiple columns
                price = listing.css('span.propertyCard-priceValue::text').get().replace("£","").replace(",","").replace(" pcm","")
                title = listing.css('meta').attrib['content'].split(" ")
                postcode  = title[-1]
                road = str(title[:-1]).replace("[","").replace("]","").replace("',","").replace(",'","").replace("'","").replace('"','')
                bedrooms = listing.xpath('div/div/div[4]/div/div[2]/a/h2').get().replace('"','').replace('<h2 class=propertyCard-title itemprop=name>','').replace('</h2>','').strip()
                numberBedrooms, type = bedrooms.split(" ", 1)
                type = str(type).replace("bedroom ","")
                id = listing.attrib["id"].replace("property-","")
                # Export
                yield{
                    "price": price,
                    "numberBedrooms": numberBedrooms,
                    "type": type,
                    "area": road,
                    "postcode": postcode,
                    "url": URL + listing.xpath('div[1]/div/div/div/div/a')
                                .attrib['href'],
                    "img": listing.css("div > div > div > div > div > div > a > div > img").attrib["src"]
                                        
                }
                
            except:
                pass