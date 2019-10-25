from rssfeed import RSSFeed

archived_feeds = []

def parseFeed(line):
    fields = line.split(',')

    url = fields[0].split(": ")[1]
    tag = fields[1].split(": ")[1]
    attribute = fields[2].split(": ")[1]

    rssFeed = RSSFeed(url, tag, attribute)

    return rssFeed

def readAllFeeds():

     f = open("rss_feeds.txt", "r")

     for line in f:
         rssFeed = parseFeed(line)
         archived_feeds.append(rssFeed)

def listAllFeeds():

    for feed in archived_feeds:
        print(feed.__repr__())

def addFeed():

    url = input("RSS feed url: ")
    tag = input("Tag name: ")
    attribute = input("Attribute name: ")
    
    rssFeed = RSSFeed(url, tag, attribute)

    archived_feeds.append(rssFeed)

    f = open ("rss_feeds.txt","a")
    f.write(rssFeed.__repr__() + '\n')
    f.close()   

    return

if __name__ == "__main__": 

    readAllFeeds()

    while True:
        print("You have next options:\n 1. list (list all rss feeds)\n 2. add (add new rss feed)\n 3. exit")
        command = input()
        if command == 'exit':
            break;
        if command == 'add':
            addFeed()
        if command == 'list':
            listAllFeeds()
   