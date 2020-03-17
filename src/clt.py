from bs4 import BeautifulSoup
import requests
import re
import os

def get_urls(f, l):
    url_list = list()
    base = 'https://rkd.nl/en/explore/images/record?filters%5Bkunstenaar%5D%5B0%5D=Mondriaan%2C+Piet&query=piet+mondrian&sort%5Bsort_startdate%5D=asc&start='
    for i in range(f, l+1):
        number = str(i)
        painting_url = base + number
        url_list.append(painting_url)
    return url_list

def get_id(soup, idpat, nanpat0, nanpat1):
    for i in range(10):
        if soup.find_all("div", {"class": 'text'})[i].string[0:8]  == 'Location':
            s = str(soup.find_all("div", {"class": 'text'})[i].next_element.next_element)
            if len(re.findall(nanpat0, s)) > 0 or len(re.findall(nanpat1, s)) > 0:
                pid = 'Unavailable'
                return pid
            pid = re.findall(idpat, s)[0]
            return pid
        
def get_title(soup):
    if soup.find(string='English title') == None:
        return 'Unavailable'
    else:
        return soup.find(string='English title').next_element.next_element.text.strip()

def get_date(soup):
    for i in range(5):
        if soup.find_all("div", {"class": 'text'})[i].string[0:5]  == 'Exact':
            date = soup.find_all("div", {"class": 'text'})[i].next_element.next_element.next_element.next_element.strip()
            return date

def get_category(soup):
    return soup.find_all('a', {'class': 'thesaurus'})[0].string

def get_image_link(soup):
    return soup.find_all('meta')[9]['content']

#----------------------------------------------------------------------------

def collect_data(first=0, last=19, outdir=None):
    
    paintings = list()
    
    url_list = get_urls(first, last)
    
    id_pat = '\d+\d'
    id_patnan_0 = '>na<'
    id_patnan_1 = 'digital'
    
    # Pull painting info from web
    for url in url_list:
        painting = dict()
        
        doc = requests.get(url)
        soup = BeautifulSoup(doc.text)
        
        pid = get_id(soup, id_pat, id_patnan_0, id_patnan_1)
        if pid == 'Unavailable':
            continue
        
        painting['id'] = pid
        painting['title'] = get_title(soup)
        painting['date'] = get_date(soup)
        painting['category'] = get_category(soup)
        painting['image_link'] = get_image_link(soup)
        
        paintings.append(painting)
        
    # Write data to outpath
    if outdir:
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        filename = os.path.join(outdir, 'paintings.txt')
        with open(filename, 'w') as fh:
            for item in paintings:
                fh.write('%s\n' % item)
        