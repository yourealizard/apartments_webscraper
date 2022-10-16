# apartments.com webscraper

This is a personal project that webscrapes data from apartments.com for a single city.  My motivation for this project was to make it a little easier to visualize the cluster of cheaper apartments.  The script in this repository scrapes the address, prices, number of bedrooms, and contact phone numbers off of apartments.com and puts it into a csv file.  

The following is a brief summary of the sort of data manipulation I do to go from the scraped data to the data visualization found here: https://public.tableau.com/app/profile/jen7417/viz/ApartmentPricesNearMe/Sheet1?publish=yes

Using the data in the csv file, I then do a bit of data manipulation using Notepad++ to parse out the minimum and maximum prices.  I also grab the longitude and latitude coordinates for each of the addresses listed in the csv file using Geocode by Awesome Table.  This is an excellent google sheets tool that can be found here: https://workspace.google.com/marketplace/app/geocode_by_awesome_table/904124517349.  Once these steps are completed, I then import the data, which is saved on an Excel file, into Tableau and put together the data visualization... and voila, a map of all the cheap(ish) apartments!
