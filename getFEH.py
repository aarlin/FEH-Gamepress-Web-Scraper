#Extract divs from fireemblem.gamepress.gg/hero/alfonse
from bs4 import BeautifulSoup
import requests

url = input("Enter a Hero name: ")
req = requests.get("https://fireemblem.gamepress.gg/hero/" + url)
data = req.text
soup = BeautifulSoup(data, "html.parser")

# Name, Stats, IV points - span
for span in soup.find_all('span'):
	#print (i.get('span'))
	print(span.string)