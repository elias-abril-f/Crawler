import json, scrapy

from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Property

from scraper.spiders.spiderZoopla import SpiderzooplaSpider
from scraper.spiders.spiderRightMove import SpiderrightmoveSpider

from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings

from multiprocessing import Process, Queue

regions = {}
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
 
    
@login_required(login_url='/login')
def scrape(request):
    #get the user and make it an object
    
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        user.property.all().delete()
        
        ########## Parameters for the search form ##########
        form = request.POST
        Rmax_beds= form["max_beds"]
        Rmin_beds = form["min_beds"]
        Rmax_price= form["max_price"]
        Rmin_price= form["min_price"]
        Rsearch= form["area"]
        Rsearch_code = regions[Rsearch]
        Rradius= form["radius"]
        #####################################################
    
        configure_logging()
        # Add spiders here
        spiders = [SpiderzooplaSpider, SpiderrightmoveSpider]
        # Run the spiders with the search attibutes obtained from the form
        for spider in spiders:
            run_spider(spider,Rsearch, Rsearch_code, Rmax_beds, Rmin_beds, Rmin_price, Rmax_price, Rradius)
            
        #read the data from the websites
        with open('./main/static/main/spiderZoopla.json', 'r') as f:
                data = json.load(f)
                with open('./main/static/main/spiderRightMove.json', 'r') as f:
                    data += json.load(f)
                    # assign the data to the object andsave it to the database
                    for item in data: 
                        property = Property(
                            price = item["price"],
                            numberBedrooms = item["numberBedrooms"],
                            type = item["type"],
                            area = item["area"],
                            postcode = item["postcode"],
                            url = item["url"],  
                            img = item["img"],
                            search = f'{Rsearch}-{Rmax_beds}-{Rmin_beds}-{Rmax_price}-{Rmin_price}-{Rradius}',
                            )
                        property.save()
                        # Add the property to the user that searched for it
                        user.property.add(property)
                        user.save()

        return HttpResponseRedirect(reverse("index"))

def index(request):
    if request.method == "GET":
        try:
            user = User.objects.get(username = request.user)
            data = user.property.all()
            return render(request, "main/index.html",{"listings": data})

            # Load the data we just scraped 
            #with open('./main/static/main/spiderZoopla.json', 'r') as f:
            #    data = json.load(f)
            #    with open('./main/static/main/spiderRightMove.json', 'r') as f:
            #        data += json.load(f)
            #        return render(request, "main/index.html",{"listings": data})
        except:
            return render(request, "main/index.html")
        
  
  
def delete(request):
    user = User.objects.get(username=request.user)
    user.property.all().delete()
    return HttpResponse ("deleted")
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
      
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "main/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "main/login.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "main/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "main/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/register.html")