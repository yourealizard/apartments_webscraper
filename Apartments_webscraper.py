from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import csv
import pandas as pd

#file name to save web scrapings from apartments.com
file_path = 'LA_apartment_webscrape.csv'
#apartments.com page for webscraping
url = 'https://www.apartments.com/los-angeles-ca/' 

#set headers to prevent being blocked
req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
#open up webpage
webpage = urlopen(req).read()
#use html parser
bs = BeautifulSoup(webpage, "html.parser")

#initialize variables to store data
addresses = []
prices= []
beds= []
amenities= []
phone_number = []

#grab every listing
li = bs.find_all('li', {'class': 'mortar-wrapper'})
iter = 0

#find property address, price range, # of beds, phone # in each listing and save to storage variables above
for listing in li: 
    new_address = listing.findChildren(['p','div'], {'class': 'property-address js-url'})
    new_prices = listing.findChildren(['p', 'div', 'span'], {'class': ['property-pricing', 'price-range', 'property-rents']})
    new_beds = listing.findChildren(['p', 'span', 'div'], {'class': ['property-beds', 'bed-range']})
    new_phone = listing.findChildren(['a'], {'class': 'phone-link js-phone'})
    if len(new_address): 
        addresses.append(new_address[0]['title'])
    else:
        addresses.append('')
    if len(new_prices): 
        prices.append(new_prices[0].contents[0])
    else:
        prices.append('')
    if len(new_beds):
        beds.append(new_beds[0].contents[0])
    else: 
        beds.append('')
    if len(new_phone):
        phone_number.append(new_phone[0]['href'])
    else:
        phone_number.append('')
    
#regular expressions to clean up the scraped phone #s
phone_number = [pn.replace('tel:', '') for pn in phone_number]
phone_number = [re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', pn) for pn in phone_number]

#write the data in storage variable to dataframe
df = pd.DataFrame()
df['Address'] = addresses
df['Prices'] = prices
df['Number of Bedrooms'] = beds
df['Phone Number'] = phone_number

#save to the output file
df.to_csv(file_path, index=False)  