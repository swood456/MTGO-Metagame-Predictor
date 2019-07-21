import scraper
import imageParse

if __name__ == "__main__":
	userList = imageParse.grabUserList()

	metagame = scraper.build_metagame(userList)

	metagameList = [(key, value) for key, value in metagame.items()]

	metagameList = sorted(metagameList, key=lambda deck: deck[1], reverse=True)

	for deck in metagameList:
		print('{}: {}%'.format(deck[0], round(deck[1] / len(userList) * 100, 2)))