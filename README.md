### Crawler (Still trying to think of a cool name)
---
# OVERVIEW
	This is a proof of concept project with Django and Scrapy. A real state aggregator including some of the most popular websites in the UK: Zoopla, RightMove and OpenRent *(at the time, more might be added)*. 
	For now, it allows you to search for renting properties in certain postcodes in London. Eventually it'll allow to search anywhere in the UK, but it'll take me some time to reverse engineer the RightMove location codes, as they don't use the search term in their URL.  

# HOW IT WORKS
	The landing page is as basic as they come. Just a fixed top bar with your search options: Area/Postcode, maximum and minimum amount of beds and price and lastly the radius of search from your original area. 

	Your search terms are part of a django form, once you submit them, since scrapy is integrated with Django as another app, this search terms are used as arguments that are passed to the spiders, one per website, and they scrape the different websites and collect the data from all the listings that match your search terms. 

	Once finished, all the data collected is sent to a custom Scrapy pipeline that turns all the items into an easy to use JSON file per website. I am currently working in get this data saved in a database and kept for a day, since the data will not take that much space but if another identical search is done, it will save a lot of time a resources. 

	After the data is dealt with and saved, the Django view redirects you to the main page again, but since now there is a lot of data to be shown, a template is used to represent each listing in a somewhat appealing manner (I haven't spent much time in this, just basic bootstrap). 
	There is also another option to load the content, with is pure javascript. Since, for now, the data is stored as a json file, javascript can deal with it easily. With the help form a jquery function to load the data, a template is used to load the data and loop through every listing. I have left the javascript code commented out in case that is an option for someone. For now I thing the use of Django templating is easier to modify. 
	
	Once loaded, that is all!! Feel free to scroll though all your new options, if you like any, click anywhere in the listing's card and it'll take you to the official listing. 
	
# FUTURE IMPROVEMENTS
- **Website selector**: I will include a way to select from which website you want to get results. 
- **User accounts**: Having a user account will allow you to save your liked listings and searches 
- **Expansion**: Reverse engineer the RightMove area/postcode codes to allow the user to use any search term and search for properties anywhere in the UK.

	
