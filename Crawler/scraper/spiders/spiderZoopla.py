import scrapy


class SpiderzooplaSpider(scrapy.Spider):
    name = 'spiderZoopla'
    allowed_domains = ['zoopla.co.uk']
    
    def __str__ (self):
        return self.name
    
    def __init__(self, *args, **kwargs):
        super(SpiderzooplaSpider, self).__init__(*args, **kwargs)
    
    def start_requests(self):
        for i in range (1, 10):
            yield scrapy.Request(f'https://www.zoopla.co.uk/to-rent/property/{self.search}/?price_frequency=per_month&search_source=refine&beds_max={self.max_beds}&beds_min={self.min_beds}&price_max={self.max_price}&price_min={self.min_price}&view_type=list&pn={i}')
        #yield scrapy.Request(f'https://www.zoopla.co.uk/to-rent/property/finsbury-park/')

    def parse(self, response):
    
        listings = response.css("div.c-jiEdYR")
        
        for listing in listings:
            try:
                
                URL = "https://www.zoopla.co.uk"
                
                price = listing.css("p.c-bTssUX::text").get().replace("pcm","").replace("£","").replace(",","").replace(" ","")
                
                title = listing.css("h2.c-hNUmYp::text").get()
                numberBedrooms, type = title.split(" bed ")
                type = type.replace(" to rent","")
                
                address = listing.css("h3.c-eFZDwI::text").get()
                address = address.split(",")
                postcode = str(address[-1])
                tmp = postcode.split(" ")
                postcode = tmp[-1]
                area2 = str(tmp[:-1])
                area = (str(address[:-1]) + area2).replace("[","").replace("]","").replace("'","").replace(",","")
                
                url = listing.css("a.c-hhFiFN").attrib["href"]
                url, trash = url.split("/?search")
                yield{
                    "price":  price,
                    "numberBedrooms": numberBedrooms,
                    "type": type,
                    "area": area,
                    "postcode": postcode,
                    "url": URL+url,
                    "img": listing.css("img.c-iIvYAS").attrib["src"]
                }
            except:
                pass
