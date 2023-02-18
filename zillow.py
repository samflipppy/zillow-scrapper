import requests
from bs4 import BeautifulSoup
import csv

# set the zipcode for which you want to find realtor information
zipcode = '12345'

# set the url to the Zillow search results page for the zipcode
url = f'https://www.zillow.com/homes/for_sale/{zipcode}/'

# send a GET request to the url and parse the HTML content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# find all the links to individual listing pages on the search results page
listing_links = soup.find_all('a', {'class': 'list-card-link'})

# create a list to hold the realtor information for each listing
realtor_info = []

# iterate through each listing link and extract the realtor information
for link in listing_links:
    listing_url = link['href']
    listing_response = requests.get(listing_url)
    listing_soup = BeautifulSoup(listing_response.content, 'html.parser')
    realtor_name = listing_soup.find('div', {'class': 'zsg-photo-card-caption'}).find('a').text.strip()
    realtor_phone = listing_soup.find('div', {'class': 'zsg-photo-card-caption'}).find('div', {'class': 'zsg-photo-card-phone'}).text.strip()
    realtor_info.append([realtor_name, realtor_phone])

# write the realtor information to a CSV file
with open(f'realtor_info_{zipcode}.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Realtor Name', 'Realtor Phone'])
    writer.writerows(realtor_info)
