import requests 
from bs4 import BeautifulSoup 
  
# arhiva iz koje se ucitavaju poodaci
archived_urls  = []
all_downloaded_links = set ()

def get_archived_urls():
    
    f = open("rss_feeds.txt", "r")
    
    for link in f:
        archived_urls.append(link)
   
    f.close()

    return

def get_downloaded_podcasts():

    f = open("downloaded_podcasts.txt", "r")

    for podcast in f:
        all_downloaded_links.add(podcast)
    
    f.close()

    return

def get_video_links(): 

    for archive_url in archived_urls:
        
        r = requests.get(archive_url) 
        soup = BeautifulSoup(r.content,'html5lib') 
        links = soup.findAll('enclosure')  
        video_links = []
           
        count = 0
    
        for link in links:
            real_link = links[count]['url']
            if (real_link.endswith('.mp3')) and  not (real_link in all_downloaded_links):
                video_links.append(real_link)
            count = count + 1
    
    return video_links 

def download_video_series(video_links): 
    
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

    get_archived_urls()
    get_downloaded_podcasts()

    video_links = get_video_links() 

    download_video_series(video_links) 
