from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import threading

class scrapeUserThread (threading.Thread):
	def __init__(self, user, metagame):
		threading.Thread.__init__(self)
		self.user = user
		self.metagame = metagame
	def run(self):
		userDecks, userTotal = scrapeUser(self.user, 'Legacy')
		addUser(self.metagame, userDecks, userTotal)

def simple_get(url):
	"""
	Attempts to get the content at `url` by making an HTTP GET request.
	If the content-type of response is some kind of HTML/XML, return the
	text content, otherwise return None.
	"""
	try:
		with closing(get(url, stream=True)) as resp:
			if is_good_response(resp):
				return resp.content # pylint: disable=no-member
			else:
				return None

	except RequestException as e:
		log_error('Error during requests to {0} : {1}'.format(url, str(e)))
		return None


def is_good_response(resp):
	"""
	Returns True if the response seems to be HTML, False otherwise.
	"""
	content_type = resp.headers['Content-Type'].lower()
	return (resp.status_code == 200 
		and content_type is not None 
		and content_type.find('html') > -1)


def log_error(e):
	"""
	It is always a good idea to log errors. 
	This function just prints them, but you can
	make it do anything.
	"""
	print(e)

def scrapeUser(userName, targetFormat):
	# TODO: some local caching (simple) to prevent massive number of hits to MTGGoldfish
	raw_html = simple_get('https://www.mtggoldfish.com/player/' + userName)
	html = BeautifulSoup(raw_html, 'html.parser')

	potentialDecks = {}
	totalDecks = 0

	# TODO: some error handling if the user has no tournaments
	for row in html.select('tr'):
		columns = row.select('td')

		if len(columns) < 1:
			continue

		stringDate = columns[0].next
		if (stringDate == '\n'): # is there a better way to determine if something is a date? Maybe by trying to parse as date and handling errors?
			continue

		eventDate = datetime.strptime(stringDate, '%Y-%m-%d %H:%M:%S %Z')

		lastMonth = datetime.now() - timedelta(weeks=4)

		if eventDate < lastMonth:
			continue

		stringFormat = columns[2].next

		if stringFormat.lower() != targetFormat.lower():
			continue

		playedDeck = columns[3].next.next
		potentialDecks[playedDeck] = potentialDecks.get(playedDeck, 0) + 1
		totalDecks += 1

	return potentialDecks, totalDecks

def addUser(baseDict, userDict, userTotal):
	if userTotal == 0:
		baseDict["Unknown"] = userDict.get("Unknown", 0) + 1

	for deck in userDict:
		deckFraction = userDict[deck] / userTotal
		baseDict[deck] = userDict.get(deck, 0) + deckFraction

def build_metagame(userList):
	metagame = {}
	userThreads = list()

	for user in userList:
		thread = scrapeUserThread(user, metagame)
		userThreads.append(thread)
		thread.start()

	for thread in userThreads:
		thread.join()

	return metagame