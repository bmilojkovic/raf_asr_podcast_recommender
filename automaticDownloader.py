import requests 
from rssfeed import RSSFeed
from bs4 import BeautifulSoup 
  
# arhiva iz koje se ucitavaju poodaci
archived_feeds =  []
all_downloaded_links = set ()

def parseFeed(line):
    fields = line.split(',')

    url = fields[0].split(": ")[1].strip()
    tag = fields[1].split(": ")[1].strip()
    attribute = fields[2].split(": ")[1].strip()

    rssFeed = RSSFeed(url, tag, attribute)

    return rssFeed


def get_archived_feeds():
    
    f = open("rss_feeds.txt", "r")
    
    for line in f:
        rssFeed = parseFeed(line)
        archived_feeds.append(rssFeed)
   
    f.close()

    return

def get_downloaded_podcasts():

    f = open("downloaded_podcasts.txt", "r")

    for podcast in f:
        all_downloaded_links.add(podcast.strip())
    
    f.close()

    return

def get_video_links(): 
    
    video_links = []
           
    for rssFeed in archived_feeds:
        r = requests.get(rssFeed.url) 
        soup = BeautifulSoup(r.content,'html.parser') 
        links = soup.findAll(rssFeed.tag)  
    
        count = 0
        added = 0

        for link in links:
            real_link = links[count][rssFeed.attribute]
            if ( '.mp3' in real_link)  and  not (real_link in all_downloaded_links):
                print(real_link)
                video_links.append(real_link)
                added = added + 1
            count = count + 1
            if added > 0:
                break

    
    return video_links 

def download_video_series(video_links): 
    
    print(video_links)

    for link in video_links: 

        if link in all_downloaded_links:
            continue

        file_name = link.split('/')[-1]    

        r = requests.get(link, stream = True) 
          
        with open(file_name, 'wb') as file1: 
            for chunk in r.iter_content(chunk_size = 1024*1024): 
                if chunk: 
                    file1.write(chunk)

        all_downloaded_links.add(link)

        f = open ("downloaded_podcasts.txt","a")
        f.write(link + '\n')
        f.close()        

    return


if __name__ == "__main__": 

    get_archived_feeds()
    get_downloaded_podcasts()

    print(all_downloaded_links)

    video_links = get_video_links() 

    download_video_series(video_links) 
    
    print(all_downloaded_links)