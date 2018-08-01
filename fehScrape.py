# Web scraper using BeautifulSoup
# mauduong

from urllib.request import urlopen
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import csv
import requests
import re

dataArray = []

def getRequest(url):
	try: 
		query_page = url
		request = requests.get(query_page)
		if (request.status_code == 200):
			page = request.text
			soup = BeautifulSoup(page, 'html.parser')
			scrapeURL(soup, url)
		else:
			log_error("Error during GET request: {0}".format(request))
	except RequestException as e:
		log_error("RequestException during {0} : {1}\n".format(url, str(e)))
	except HTMLParseError as e:
		log_error("HTMLParseError during {0} : {1}\n".format(url, str(e)))
	except ImportError as e:
		log_error("ImportError during {0} : {1}\n".format(url, str(e)))
	
def scrapeURL(soup, url):
	heroNameUpper = url.replace('https://fireemblem.gamepress.gg/hero/', '').upper()
	print('Attempting scrape - {0}'.format(heroNameUpper))
	
	try: 
		getName(soup)
		getStats(soup)
		getSkills(soup)
		dataArray.append('\n')
		try:
			csvWrite(dataArray)
		except IOError as e:
			log_error("IO Error during {0}\n".format(str(e)))
	except Exception as e:
		log_error("Error during scraping {0} : {1}\n".format(url, str(e)))
		
# Get a single Hero's name and title
def getName(soup):
	try: 
		for name in soup.find('table', attrs={'id': 'hero-details-table'}).find('span'):
			title = name.findNext('span').get_text().replace('-', '').strip()
			
		dataArray.append(name)
		dataArray.append(title)
	except Exception as e:
		log_error("Error during name and title scraping {0} : {1}\n".format(soup, str(e)))

# Function to gather NEUTRAL IV stats of the specified Hero
def getStats(soup):
	try:
		for headerStats in soup.find_all('div', attrs={'class': 'header-stats'}):
			head = headerStats.get_text().strip()
			dataArray.append(head)
	except Exception as e:
		log_error("Error during IV variation scraping {0} : {1}\n".format(soup, str(e)))

def getSkills(soup):
	try:
		# Get all available weapons of the specified Hero
		for weapon in soup.find_all('td', attrs={'headers': 'view-title-table-column', 'class': 
		'views-field views-field-title views-field-field-weapon-effect views-field-field-star-defaults views-field-field-stars views-field-description__value'}):
			weaponName = weapon.get_text().strip()
			weaponDesc = "WEAPON: " + weaponName
			dataArray.append(weaponDesc)
			
		# Get all available support skills
		for assist in soup.find_all('td', attrs={'headers': 'view-title-table-column--3', 'class': 
		'views-field views-field-title views-field-field-command-skill-effect views-field-field-star-defaults views-field-field-stars'}):
			assistName = assist.get_text().strip()
			assistDesc = "SUPPORT: " + assistName
			dataArray.append(assistDesc)
			
		# Get all available specials of the specified Hero
		for special in soup.find_all('td', attrs={'headers': 'view-title-table-column--3', 'class':
		'views-field views-field-title views-field-field-special-skill-effect views-field-field-star-defaults views-field-field-stars views-field-description__value'}):
			specialName = special.get_text().strip()
			specialDesc = "SPECIAL: " + specialName
			dataArray.append(specialDesc)
		
		# Get all available passive A, B, C skills of the specified Hero
		for passive in soup.find_all('td', attrs={'headers': 'view-field-passive-skill-icon-table-column', 'class': 
		'views-field views-field-field-passive-skill-icon views-field-title views-field-field-passive-skills-effect views-field-field-stars views-field-description__value'}):
			passiveName = passive.get_text().strip()
			passiveDesc = passiveName
			dataArray.append(passiveDesc)
			
	except Exception as e:
		log_error("Error during Skills scraping {0} : {1}\n".format(soup, str(e)))

def csvWrite(dataArray):
	# Save data to csv for later retrieval
	with open('fehcsv.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		for i in dataArray:
			writer.writerow([i])
			
"""def displayStatus(request):
	print('Displaying HTTP Request')
	print(request.status_code)
	print(request.headers['content-type'])
	print('\n')"""
	
# Prints any exception that arises
def log_error(e):
	print(e)

