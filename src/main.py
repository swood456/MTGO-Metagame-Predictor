import scraper

if __name__ == "__main__":
	# placeholder cardcoded data from 7/1 legacy challenge
	testUsers = ['Julian23', 'Bryant_Cook', 'Bahra', 'Breca', 'CryptomancerRB', 'DNSolver', 'FlyingTempest', 'NoGoodTsuna', 'wakarock', 'jjkbb2005', 'Mzfroste', 'ArmyofThalia', '_maddy', 'Lagerbon', 'ApolloTwelve', 'Pische10']

	metagame = scraper.build_metagame(testUsers)

	metagameList = [(key, value) for key, value in metagame.items()]

	metagameList = sorted(metagameList, key=lambda deck: deck[1], reverse=True)
   
	for deck in metagameList:
		print('{}: {}%'.format(deck[0], round(deck[1] / len(testUsers) * 100, 2)))