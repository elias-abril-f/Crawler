from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from scraper.spiders.spiderZoopla import SpiderzooplaSpider
from scraper.spiders.spiderRightMove import SpiderrightmoveSpider

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging, logging
from scrapy.utils.project import get_project_settings
from scrapy.settings import Settings
import json, scrapy



from multiprocessing import Process, Queue


regionsJson = '{"E1":744,"MileEnd":744,"Stepney":744,"Whitechapel":744,"E2":755,"Bethnal Green":755,"Shoreditch":755,"E3":756,"Bow":756,"Bromley-by-Bow":756,"E4":757,"Chingford":757,"Highams Park":757,"E5":758,"Clapton":758,"E6":759,"East Ham":759,"Beckton":759,"E7":760,"Forest Gate":760,"Upton Park":760,"E8":762,"Hackney":762,"Dalston":762,"E9":763,"Hackney":763,"Homerton":763,"E10":745,"Leyton":745,"E11":746,"Leytonstone":746,"E12":747,"Manor Park":747,"E13":748,"Plaistow":748,"E14":749,"Isle of Dogs":749,"Millwall":749,"Poplar":749,"E15":750,"Stratford":750,"West Ham":750,"E16":751,"Canning Town":751,"North Woolwich":751,"E17":752,"Walthamstow":752,"E18":753,"South Woodford":753,"E20":6110,"Olympic Park":6110,"Stratford":6110,"N1":1666,"Barnsbury":1666,"Canonbury":1666,"Islington":1666,"N2":1677,"East Finchley":1677,"N3":1681,"Finchley Central":1681,"N4":1682,"Finsbury Park":1682,"Manor House":1682,"N5":1683,"Highbury":1683,"N6":1684,"Highgate":1684,"N7":1685,"Holloway":1685,"N8":1686,"Crouch End":1686,"Hornsey":1686,"N9":1687,"Lower Edmonton":1687,"N10":1667,"Muswell Hill":1667,"N11":1668,"Friern Barnet":1668,"New Southgate":1668,"N12":1669,"North Finchley":1669,"Woodside Park":1669,"N13":1670,"Palmers Green":1670,"N14":1671,"Southgate":1671,"N15":1672,"Seven Sisters":1672,"N16":1673,"Stamford Hill":1673,"Stoke Newington":1673,"N17":1674,"Tottenham":1674,"N18":1675,"Upper Edmonton":1675,"N19":1676,"Archway":1676,"Tufnell Park":1676,"N20":1678,"Totteridge":1678,"Whetstone":1678,"N21":1679,"Winchmore Hill":1679,"N22":1680,"Alexandra Palace":1680,"WoodGreen":1680}'
regions = json.loads(regionsJson)

def run_spider(spider, search, search_code, max_beds, min_beds, min_price, max_price, radius):
    def f(q):
        try:
            settings = get_project_settings()
            runner = CrawlerRunner(settings)
            deferred = runner.crawl(spider,search=search, search_code = search_code, max_beds=max_beds, min_beds=min_beds, min_price=min_price, max_price=max_price, radius=radius)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()
    if result is not None:
        raise result

def scrape(request):
    if request.method == "POST":
        
        ########## Parameters for the search form ##########
        form = request.POST
        max_beds= form["max_beds"]
        min_beds = form["min_beds"]
        max_price= form["max_price"]
        min_price= form["min_price"]
        search= form["area"]
        search_code = regions[search]
        radius= form["radius"]
        #####################################################
        
        configure_logging()
        # Add spiders here
        spiders = [SpiderzooplaSpider, SpiderrightmoveSpider]
        for spider in spiders:
            run_spider(spider,search, search_code, max_beds, min_beds, min_price, max_price, radius)
        
        return HttpResponseRedirect(reverse("index"))

def index(request):
    if request.method == "GET":
        try:
            # Load the data we just scraped 
            with open('./main/static/main/spiderZoopla.json', 'r') as f:
                data = json.load(f)
                with open('./main/static/main/spiderRightMove.json', 'r') as f:
                    data += json.load(f)
                    return render(request, "main/index.html",{"listings": data})
        except:
            return render(request, "main/index.html")