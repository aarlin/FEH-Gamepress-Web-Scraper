#Scraper
from basicScrape import getRequest
import requests

while True:
	exitPrompt = "exit"
	print("Type in \"exit\" to quit without quotation marks")
	userInput = input("Enter a Hero's name: ").lower()
	
	# Terrible code but it works
	if userInput == "" or userInput == exitPrompt:
		print("You have exited the script")
		break
	else:
		url = ("https://fireemblem.gamepress.gg/hero/" + userInput)
		
	getRequest(url)
	
	
