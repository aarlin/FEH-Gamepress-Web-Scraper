# Web scraper using BeautifulSoup
# mauduong

from urllib.request import urlopen
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from html.parser import HTMLParser
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
		getIVSet(soup)
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
		origin = soup.find('div', {'class': 'field field--name-field-origin field--type-entity-reference field--label-hidden field__items'})
		origin = origin.findNext('div', attrs={'class': 'field__item'}).get_text()
		for name in soup.find('table', attrs={'id': 'hero-details-table'}).find('span'):
			title = name.findNext('span').get_text().replace('-', '').strip()
			
		dataArray.append(name)
		dataArray.append(title)
		dataArray.append("Origin: " + origin + '\n')
	except Exception as e:
		log_error("Error during name and title scraping {0} : {1}\n".format(soup, str(e)))

# Function to gather NEUTRAL IV stats of the specified Hero
def getStats(soup):
	try:
		totalBST = soup.find('span', attrs={'class': 'max-stats-number'}).get_text().strip()
		totalBST = "Base Stats Total: " + totalBST
		dataArray.append(totalBST)
		for headerStats in soup.find_all('div', attrs={'class': 'header-stats'}):
			head = headerStats.get_text().strip()
			dataArray.append(head)
	except Exception as e:
		log_error("Error during IV variation scraping {0} : {1}\n".format(soup, str(e)))

def getSkills(soup):
	try:
		# Weapons available for a specific Hero
		for weapon in soup.find_all('td', attrs={'headers': 'view-title-table-column', 'class': 
		'views-field views-field-title views-field-field-weapon-effect views-field-field-star-defaults views-field-field-stars views-field-description__value'}):
			weaponSP = weapon.findNext('td', {'headers': 'view-field-weapon-skills-sp-cost-table-column'}).get_text()
			weaponRNG = weapon.findNext('td', {'headers': 'view-field-weapon-range-table-column'}).get_text()
			weaponMT = weapon.findNext('td', {'headers': 'view-field-weapon-power-table-column'}).get_text()
			weaponName = weapon.get_text().strip()
			weaponDesc = "WEAPON: " + weaponName + " SP: " + weaponSP + " RNG: " + weaponRNG + " MIGHT: " + weaponMT
			dataArray.append(weaponDesc)
			
		# Weapon upgrades available for a specific Hero
		for upgrade in soup.find_all('td', attrs={'headers': 'view-title-table-column--2', 'class': 'views-field views-field-title views-field-field-weapon-effect'}):
			weaponUpgradeName = upgrade.get_text().strip()
			weaponUpgradeHP = upgrade.findNext('td', {'headers': 'view-field-refinery-hp-bonus-table-column'}).get_text()
			weaponUpgradeSP = upgrade.findNext('td', {'headers': 'view-field-weapon-skills-sp-cost-table-column--2'}).get_text()
			weaponUpgradeRNG = upgrade.findNext('td', {'headers': 'view-field-weapon-range-table-column--2'}).get_text()
			weaponUpgradeMT = upgrade.findNext('td', {'headers': 'view-field-weapon-power-table-column--2'}).get_text()
			weaponUpgradeDesc = "UPGRADES: " + weaponUpgradeName + " HP: " + weaponUpgradeHP + " SP: " + weaponUpgradeSP + " RNG: " + weaponUpgradeRNG + " MIGHT: " + weaponUpgradeMT
			dataArray.append(weaponUpgradeDesc)
		
		# Get all available support skills
		for assist in soup.find_all('td', attrs={'headers': 'view-title-table-column--3', 'class': 
		'views-field views-field-title views-field-field-command-skill-effect views-field-field-star-defaults views-field-field-stars'}):
			assistRNG = assist.findNext('td', {'headers': 'view-field-command-skill-range-table-column'}).get_text()
			assistSP = assist.findNext('td', {'headers': 'view-field-command-skills-sp-requirem-table-column'}).get_text()
			assistName = assist.get_text().strip()
			assistDesc = "SUPPORT: " + assistName + " RNG: " + assistRNG + " SP: " + assistSP
			dataArray.append(assistDesc)
		
		# Available default specials for a specific Hero
		for special in soup.find_all('td', attrs={'headers': 'view-title-table-column--3', 'class':
		'views-field views-field-title views-field-field-special-skill-effect views-field-field-star-defaults views-field-field-stars views-field-description__value'}):
			specialSP = special.findNext('td', {'headers': 'view-field-special-skills-sp-cost-table-column'}).get_text()
			specialTurns = special.findNext('td', {'headers': 'view-field-special-skill-turn-require-table-column'}).get_text()
			specialName = special.get_text().strip()
			specialDesc = "SPECIAL: " + specialName + " SP: " + specialSP + " TURNS: " + specialTurns
			dataArray.append(specialDesc)
		
		# All available passive A, B, C skills for a specific Hero
		for passive in soup.find_all('td', attrs={'headers': 'view-field-passive-skill-icon-table-column', 'class': 
		'views-field views-field-field-passive-skill-icon views-field-title views-field-field-passive-skills-effect views-field-field-stars views-field-description__value'}):
			passiveSP = passive.findNext('td', {'headers': 'view-field-passive-skills-sp-cost-table-column'}).get_text()
			passiveSlot = passive.findNext('td', {'headers': 'view-field-passive-slot-table-column'}).get_text()
			passiveName = passive.get_text().strip()
			passiveDesc = passiveSlot + " SKILL: " + passiveName + " SP: " + passiveSP 
			dataArray.append(passiveDesc)
		
	except Exception as e:
		log_error("Error during Skills scraping {0} : {1}\n".format(soup, str(e)))

# Get IV set from Hero
def getIVSet(soup):
	try:
		hpIV = soup.find('div', {'class': 'field field--name-field-hp-iv-importance field--type-entity-reference field--label-hidden field__item'})
		atkIV = soup.find('div', {'class': 'field field--name-field-atk-iv-importance field--type-entity-reference field--label-hidden field__item'})
		spdIV = soup.find('div', {'class': 'field field--name-field-spd-iv-importance field--type-entity-reference field--label-hidden field__item'})
		defIV = soup.find('div', {'class': 'field field--name-field-def-iv-importance field--type-entity-reference field--label-hidden field__item'})
		resIV = soup.find('div', {'class': 'field field--name-field-res-iv-importance field--type-entity-reference field--label-hidden field__item'})

		hpValuation = hpIV.findNext('div', class_=re.compile('field')).get_text().strip()
		atkValuation = atkIV.findNext('div', class_=re.compile('field')).get_text().strip()
		spdValuation = spdIV.findNext('div', class_=re.compile('field')).get_text().strip()
		defValuation = defIV.findNext('div', class_=re.compile('field')).get_text().strip()
		resValuation = resIV.findNext('div', class_=re.compile('field')).get_text().strip()
		
		dataArray.append('HP ' + hpValuation)
		dataArray.append('ATK ' + atkValuation)
		dataArray.append('SPD ' + spdValuation)
		dataArray.append('DEF ' + defValuation)
		dataArray.append('RES ' + resValuation)
	except Exception as e:
		log_error("Error during IV variation scraping {0} : {1}\n".format(soup, str(e)))

def csvWrite(dataArray):
	# Save data to csv for later retrieval
	with open('fehcsv.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, lineterminator='\n')
		#writer.writerow(dataArray)
		for i in dataArray:
			writer.writerow([i])
			
# Prints any exception that arises
def log_error(e):
	print(e)

