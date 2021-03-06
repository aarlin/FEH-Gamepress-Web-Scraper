# Main script that calls a function to gather data
# mauduong
from fehScrape import getRequest
from fehScrape import log_error
from requests import get
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re


heroArray = ['abel', 'adrift-camilla', 'adrift-corrin-f', 'adrift-corrin-m', 'alfonse', 'alm', 'amelia', 'anna', 'arden', 'ares', 'arthur', 'arvis', 'athena', 'aversa', 'ayra', 'azama', 'azura', 'azura-young'
	'barst', 'bartre', 'berkut', 'beruka', 'black-knight', 'boey', 'brady',
    'brave-alm', 'brave-camilla', 'brave-celica', 'brave-eliwood', 'brave-ephraim', 'brave-hector', 'brave-ike', 'brave-lucina', 'brave-lyn', 'brave-micaiah', 'brave-roy', 
	'brave-veronica', 'bridal-caeda', 'bridal-charlotte', 'bridal-cordelia', 'bridal-fjorm', 'bridal-louise', 'bridal-lyn', 'bridal-ninian', 'bridal-sanaki', 'bridal-sigrun', 'bridal-tanith', 'bridal-tharja',
	'byleth-f', 'byleth-m',
	'caeda', 'cain', 'caineghis', 'camilla', 'camus', 'canas', 'catria', 'cecilia', 'celica', 'cherche', 'chrom', 'clair', 'clarine', 'clarisse', 'claude', 'clive',  'cordelia', 'corrin-f', 'corrin-m', 'cynthia',
	'death-knight', 'deirdre', 'delthea', 'dimitri', 'donnel', 'dorcas', 'draug', 
	'edelgard', 'effie', 'eir', 'eirika', 'eirika-sm', 'eldigan', 'elincia', 'elise', 'eliwood', 'eliwood-la', 'ephraim', 'est', 'ethlyn', 'chrome', 
	'fae', 'faye', 'felicia', 'finn', 'fir', 'fjorm', 'flora', 'florina', 'frederick', 
	'fallen-berkut', 'fallen-celica', 'fallen-corrin-f', 'fallen-delthea', 'fallen-hardin', 'fallen-mareeta',  'fallen-robin-m', 'fallen-takumi', 'fallen-tiki-young', 
	'gaius', 'garon', 'genny', 'gerome', 'gharnef', 'gordin', 'gray', 'groom-marth', 'groom-pent', 'gunnthra', 'gunter', 'gwendolyn', 
	'halloween-henry', 'halloween-jakob', 'halloween-kagero', 'halloween-mia', 'halloween-myrrh', 'halloween-niles', 'halloween-nowi', 'halloween-sakura', 
	'haar', 'hana', 'hawkeye', 'hector', 'hector-la', 'helbindi', 'henry', 'hilda', 'hinata', 'hinoka', 'hinoka-wf', 'hrid',
	'hoshidan-summer-xander', 'hoshidan-summer-elincia', 'hoshidan-summer-ryoma', 'hoshidan-summer-micaiah',
	'hostile-springs-elise', 'hostile-springs-hinoka', 'hostile-springs-ryoma', 'hostile-springs-sakura',
	'hubert',
	'idunn', 'ike', 'innes', 'ishtar', 
	'jaffar', 'jagen', 'jakob', 'jamke', 'jeorge', 'joshua', 'julia', 'julius',
	'kaden', 'kagero', 'kana-f', 'kana-m', 'karel', 'karla', 'katarina', 'kaze', 'keaton', 'kjelle', 'klein', 'kliff', 'kronya',
	'lachesis', 'laegjarn', 'laevatein', 'larachel', 'laslow', 'leanne', 'legault', 
	'legendary-azura', 'legendary-eirika', 'legendary-eliwood', 'legendary-ephraim', 'legendary-hector', 'legendary-ike', 'legendary-lucina', 'legendary-lyn', 'legendary-math', 'legendary-robin-f', 'legendary-roy', 'legendary-ryoma', 'legendary-tiki-young',
	'legion', 'leif', 'lene', 'leo', 'leon', 'lethe', 'lewyn', 'libra', 'lilina', 'lilina-la', 'linde', 'linus', 'lissa', 'lloyd', 'loki', 'lonqu', 'lucina', 'lucius', 'lugh', 'lukas', 'luke', 'lute', 'lyn', 'lyn-la', 
	'lyon', 
	'mae', 'maria', 'maribelle', 'marisa', 'marth', 'masked-marth', 'mathilda', 'matthew', 'mercedes', 'merric', 'mia', 'micaiah', 'michalis', 'mikoto', 'minerva', 'mist', 'mordecai', 'morgan-f', 'morgan-m', 'myrrh', 
	'naesala', 'naga', 'nah', 'nailah', 'nanna', 'narcian', 'navarre', 'nephenee', 
	'new-year-azura', 'new-year-camilla', 'new-year-corrin-m', 'new-year-fjorm', 'new-year-gunnthra', 'new-year-hrid', 'new-year-laegjarn', 'new-year-laevatein', 'new-year-takumi', 
	'niles', 'nina', 'ninian', 'nino', 'nino-sf', 'nowi', 
	'oboro', 'odin', 'ogma', 'oliver', 'olivia', 'olivia-yt', 'olwen', 'olwen-wt', 'ophelia', 'oscar', 'owain',
	'palla', 'panne', 'performing-azura', 'performing-inigo', 'performing-olivia', 'performing-shigure', 'peri', 'petra', 'priscilla', 
	'picnic-genny', 'picnic-felicia', 'picnic-flora', 'picnic-leo', 'picnic-lukas',
	'quan',
	'raigh', 'ranulf', 'raven', 'rebecca', 'reinhardt', 'reinhardt-wt', 'reyson', 'rhajat', 'robin-f', 'robin-m', 'roderick', 'roy', 'roy-la', 'rutger', 'ryoma', 
	'saber', 'saias', 'saizo', 'sakura', 'sanaki', 'selena', 'seliph', 'selkie', 'serra', 'seth', 'setsuna', 'shanna', 'sharena', 'sheena', 'shigure', 'shiro', 'siegbert', 'silas', 'silvia', 'soleil', 
	'sonya', 'sophia', 'soren', 'sothe', 'sothis', 
	'spring-alfonse', 'spring-bruno', 'spring-camilla', 'spring-catria', 'spring-chrom', 'spring-felicia', 'spring-flora', 'spring-genny', 'spring-kagero', 'spring-leo', 'spring-loki', 'spring-lukas', 'spring-lucina', 'spring-palla', 'spring-marisa', 'spring-sharena', 'spring-veronica', 'spring-xander', 'stahl', 
	'subaki', 'sue', 'sully', 'sumia', 'summer-camilla', 'summer-cordelia', 'summer-corrin-f', 'summer-elise', 'summer-fiora', 'summer-frederick', 'summer-frederick', 'summer-gaius', 'summer-gunnthra', 'summer-helbindi', 'summer-innes', 'summer-laegjarn', 'summer-laevatein',
	'summer-leo', 'summer-lilina', 'summer-linde', 'summer-lyn', 'summer-noire', 'summer-robin-f', 'summer-takumi', 'summer-tana', 'summer-tiki-adult', 'summer-tiki-young', 'summer-ursula', 'summer-wolt', 'summer-xander', 'summer-ylgr', 'surtr',
	'tailtiu', 'takumi', 'tana', 'tharja', 'thea', 'tibarn', 'tiki-adult', 'tiki-young', 'titania', 'tobin', 
	'ursula', 
	'valter', 'velouria', 'virion',
	'valentines-greil', 'valentines-ike', 'valentines-mist', 'valentines-soren', 'valentines-titania',
	'walhart', 'winter-cecilia', 'winter-chrom', 'winter-eirika', 'winter-ephraim', 'winter-fae', 'winter-lissa', 'winter-robin', 'winter-tharja', 'wrys', 
	'xander',
	'yarne', 'yglr', 'yune',
	'zelgius', 'zephiel']
		
#heroArray = ['alfonse', 'sharena', 'anna']

url = "https://fireemblem.gamepress.gg/hero/"

for i, value in enumerate(heroArray):
	try:
		concatURL = url + value;
		getRequest(concatURL)
	except IndexError as e:
		log_error("Error during heroArray value - {0} : {1}".format(value, str(e)))
