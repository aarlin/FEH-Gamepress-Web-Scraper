# Main script that calls a function to gather data
# mauduong
from fehScrape import getRequest
from fehScrape import log_error
from requests import get
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re


heroArray = ['abel','alfonse', 'alm', 'amelia', 'anna', 'arden', 'ares', 'arthur', 'arvis', 'athena', 'ayra', 'azama', 'azura', 
	'barst', 'bartre', 'berkut', 'beruka', 'black-knight', 'boey', 'brave-celica', 'brave-ephraim', 'brave-hector', 'brave-ike', 'brave-lucina', 'brave-lyn', 'brave-roy', 
	'brave-veronica', 'bridal-caeda', 'bridal-charlotte', 'bridal-cordelia', 'bridal-lyn', 'bridal-ninian', 'bridal-sanaki', 'bridal-tharja', 
	'caeda', 'cain', 'camilla', 'camus', 'canas', 'catria', 'cecilia', 'celica', 'cherche', 'chrom', 'clair', 'clarine', 'clarisse', 'clive', 'cordelia', 'corrin-f', 'corrin-m', 
	'deirdre', 'delthea', 'donnel', 'dorcas', 'draug', 
	'effie', 'eirika', 'eirika-sm', 'eldigan', 'elincia', 'elise', 'eliwood', 'eliwood-la', 'ephraim', 'est', 'chrome', 
	'fae', 'fallen-celica', 'fallen-hardin', 'fallen-robin-m', 'fallen-takumi', 'faye', 'felicia', 'finn', 'fir', 'fjorm', 'florina', 'frederick', 
	'gaius', 'genny', 'gerome', 'gordin', 'gray', 'groom-marth', 'gunnthra', 'gunter', 'gwendolyn', 
	'halloween-henry', 'halloween-jakob', 'halloween-nowi', 'halloween-sakura', 'hana', 'hawkeye', 'hector', 'hector-la', 'henry', 'hinata', 'hinoka', 'hinoka-wf',
	'hoshidan-summer-xander', 'hoshidan-summer-elincia', 'hoshidan-summer-ryoma', 'hoshidan-summer-micaiah',
	'ike', 'innes', 'ishtar', 
	'jaffar', 'jagen', 'jakob', 'jeorge', 'joshua', 'julia', 'julius',
	'kagero', 'kana-f', 'kana-m', 'karel', 'karla', 'katarina', 'kaze', 'klein', 
	'larachel', 'lachesis', 'laslow', 'legault', 
	'legendary-ephraim', 'legendary-hector', 'legendary-ike', 'legendary-lucina', 'legendary-lyn', 'legendary-math', 'legendary-robin-f', 'legendary-ryoma', 
	'legion', 'leif', 'lene', 'leo', 'leon', 'libra', 'lilina', 'lilina-la', 'linde', 'linus', 'lissa', 'lloyd', 'lonqu', 'lucina', 'lucius', 'lukas', 'luke', 'lute', 'lyn', 'lyn-la', 
	'lyon', 
	'mae', 'maria', 'maribelle', 'marisa', 'marth', 'masked-marth', 'mathilda', 'matthew', 'merric', 'mia', 'micaiah', 'michalis', 'minerva', 'mist', 'morgan-f', 'morgan-m', 'myrrh', 
	'nanna', 'narcian', 'navarre', 'nephenee', 'new-year-azura', 'new-year-camilla', 'new-year-corrin-m', 'new-year-takumi', 'niles', 'ninian', 'nino', 'nino-sf', 'nowi', 
	'oboro', 'odin', 'ogma', 'oliver', 'olivia', 'olivia-yt', 'olwen', 'olwen-wt', 'oscar',
	'palla', 'performing-azura', 'performing-inigo', 'performing-olivia', 'performing-shigure', 'peri', 'priscilla', 
	'raigh', 'raven', 'rebecca', 'reinhardt', 'reinhardt-wt', 'rhajat', 'robin-f', 'robin-m', 'roderick', 'roy', 'roy-la', 'ryoma', 
	'saber', 'saias', 'saizo', 'sakura', 'sanaki', 'selena', 'seliph', 'serra', 'seth', 'setsuna', 'shanna', 'sharena', 'sheena', 'shigure', 'shiro', 'siegbert', 'soleil', 'sonya', 
	'sophia', 'soren', 'sothe', 'spring-alfonse', 'spring-camilla', 'spring-catria', 'spring-chrom', 'spring-kagero', 'spring-lucina', 'spring-sharena', 'spring-xander', 'stahl', 
	'subaki', 'sully', 'sumia', 'summer-camilla', 'summer-cordelia', 'summer-corrin-f', 'summer-elise', 'summer-frederick', 'summer-frederick', 'summer-gaius', 'summer-innes', 
	'summer-leo', 'summer-linde', 'summer-noire', 'summer-robin-f', 'summer-takumi', 'summer-tana', 'summer-tiki-adult', 'summer-tiki-young', 'summer-xander', 
	'tailtiu', 'takumi', 'tana', 'tharja', 'tiki-adult', 'tiki-young', 'titania', 'tobin', 
	'ursula', 
	'valter', 'virion',
	'walhart', 'winter-chrom', 'winter-lissa', 'winter-robin', 'winter-tharja', 'wrys', 
	'xander', 
	'zelgius', 'zephiel']
		
#heroArray = ['alfonse', 'sharena', 'anna']

url = "https://fireemblem.gamepress.gg/hero/"

for i, value in enumerate(heroArray):
	try:
		concatURL = url + value;
		getRequest(concatURL)
	except IndexError as e:
		log_error("Error during heroArray value - {0} : {1}".format(value, str(e)))