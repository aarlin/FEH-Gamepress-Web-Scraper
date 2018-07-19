#Simple web scrape with BeautifulSoup
from urllib.request import urlopen
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import requests

dataArray = []

def getRequest(url):
	try:
		query_page = url
		request = requests.get(query_page)
		displayStatus(request)
		if (request.status_code == 200):
			page = request.text
			soup = BeautifulSoup(page, 'html.parser')
			scrapeURL(soup, url)
		else:
			log_error("Error during GET request: {0}".format(request))
	except RequestException as e:
		log_error("Error during {0} : {1}\n".format(url, str(e)))

def scrapeURL(soup, url):
	print('Attempting scrape - {0}'.format(url))
	
	for name in soup.find('table', attrs={'id': 'hero-details-table'}).find('span'):
		title = name.findNext('span').get_text().replace('-', '').strip()
		
	dataArray.append(name)
	dataArray.append(title)
	
	for stats in soup.find_all('span', attrs={'class': 'stat-text'}):
		formattedStats = stats.get_text()
		dataArray.append(formattedStats)
	
	dataArray.append('\n')
	try:
		csvWrite(dataArray)
	except Exception as e:
		log_error("Error during writing CSV {0} : {1}\n".format(dataArray, str(e)))
	
	print('Writing to csv file\n')
	
def csvWrite(dataArray):
	# Save data to csv for later retrieval
	with open('fehcsv.csv', 'a', newline='') as csvfile:
		writer = csv.writer(csvfile)
		for i in dataArray:
			writer.writerow([i])
			
def displayStatus(request):
	print('Displaying HTTP Request')
	print(request.status_code)
	print(request.headers['content-type'])
	print('\n')
	
# Prints any exception that arises
def log_error(e):
	print(e)

