from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import csv
import pandas as pd
import numpy as np

#file name to save web scrapings from apartments.com; expects user to write to a .csv file
file_path = 'apartment_webscrape.csv'
#apartments.com page for webscraping
url = 'https://www.apartments.com/los-angeles-ca/' 

#set headers to prevent being blocked
req = Request(url, headers = {'User-Agent': 'Mozilla/5.0'})
#open up webpage
webpage = urlopen(req).read()
#use html parser
bs = BeautifulSoup(webpage, "html.parser")

#DEBUG
# with open("webpage_scrapings_LA.txt", "w", encoding = 'utf-8') as file:   
#     # prettify the soup object and convert it into a string  
#     file.write(str(bs.prettify()))
#bs = BeautifulSoup(open("webpage_scrapings.txt").read(), "html.parser")

#grab the number of pages 
page_range = bs.find_all('span', class_="pageRange")
if (page_range): 
    temp_string = re.search(r'.* of \d*', page_range[0].contents[0]).string
    temp_string = re.sub(r'.* of (\d*)', r'\1', temp_string).strip()
    page_max = type(int(temp_string))
else:
    for i in range(5,1,-1):
        temp_string = bs.find_all('a', {'data-page': str(i)})
        if(temp_string):
            break
    temp_string = temp_string[0].contents[0].strip()
    page_max = int(temp_string)

#loop through each webpage to scrape
for i in range(1,page_max+1):
    
    #initialize variables to store data
    addresses = []
    prices= []
    beds= []
    amenities= []
    phone_number = []

    if i!=1:
        req = Request(url+str(i)+'/', headers = {'User-Agent': 'Mozilla/5.0'})
        #open up webpage
        webpage = urlopen(req).read()
        bs = BeautifulSoup(webpage, "html.parser")
    
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
    
    #removing empty rows from dataframe
    df['Address'].replace('', np.nan, inplace=True)
    df.dropna(subset=['Address'], inplace=True)
    
    #save to the output file
    if i==1: 
        df.to_csv(file_path, index=False)  
    else:
        df.to_csv(file_path, mode='a', index=False, header=False)