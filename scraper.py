from bs4 import BeautifulSoup
from urllib.request import urlopen
import json
from threading import Thread

start_url = 'https://kitabosunnat.com/get-searched-book?searchword='
current_page = 1
books_template = {
    '0' : {
        'name' : 'a',
        'desc' : 'b',
        'author' : 'c',
        'publisher' : 'd',
        'thumbl' : 'http...',
        'link' : 'http...'
    }
}
books = {}

def checkjson():
  try:
    with open(filename) as f:
      return True
  except FileNotFoundError:
    with open(filename, 'w') as f:
      return False
  except:
    return False
 
def dumpjson(data):
  with open('pages_1_30.json', 'w') as f:
    json.dump(data, f)
    
def uopen(url):
    try:
        return urlopen(url)
    except:
        print('retrying...')
        open(url)
    

def scrapeBookData(book):
    # Scrape book's general data
    print('Here comes the book...')
    bid = book.select('.listingTop .numberRight span ~ span')[0].get_text().strip()
    bname = book.select('h4')[0].get_text().strip()
    bdesc = book.select('.listCont')[0].get_text().strip()
    bauthor = book.select('.listingTop h3 a')[0].get_text().strip()
    bpub = book.select('.listPublisher a')[0].get_text().strip()
    bthumb = book.select('a.listingImg img')[0]['src']
    blink = book.select('.listingMain h4 a')[0]['href']
    bdlink = openBookLink(blink)
    books[bid] = {
        'name' : bname,
        'description' : bdesc,
        'author' : bauthor,
        'publisher' : bpub,
        'thumbnail' : bthumb,
        'link' : bdlink
    }
    print('Done with book: ', bid)

def openBookLink(link):
    # Scrape book's download link
    print('Following link: ' + link)
    bobj = BeautifulSoup(uopen(link).read())
    blink = bobj.select('span.sf-dump-str')[0].get_text()
    return blink

def processResults(bs):
    # Process results page
    print('Now on page: %d' % current_page)
    with open('index.html', 'w') as f:
        f.write(str(bs.html))
    books = bs.select('ul.serachList li')
    print('Found %d books' % (len(books)) )
    
    # multithreading
    threads = [Thread(target=scrapeBookData, args=(book,)) for book in books]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    
#     for book in books:
#         scrapeBookData(book)

# starting page
html = uopen(start_url)
bs = BeautifulSoup(html.read())
for page in range(2, 31):
    processResults(bs)
    next_url = start_url + '&page=' + str(page)
    bs = BeautifulSoup(uopen(next_url).read() )
    current_page = page

print('Now saving data in json')
dumpjson(books)
print('Done...')
