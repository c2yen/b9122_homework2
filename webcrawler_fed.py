from bs4 import BeautifulSoup
import urllib.request

seed_url = "https://www.federalreserve.gov/newsevents/pressreleases.htm"
real_url = 'https://www.federalreserve.gov/newsevents/pressreleases/'

urls = [seed_url]
seen = [seed_url]
opened = []
covid = []

maxNumUrl = 150
print("Starting with url="+str(urls))

while len(urls) > 0 and len(opened) < maxNumUrl:
    try:
        curr_url=urls.pop(0)
        req = urllib.request.Request(curr_url,headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urllib.request.urlopen(req).read()
        opened.append(curr_url)

    except Exception as ex:
        print("Unable to access= "+curr_url)
        print(ex)
        continue

    soup = BeautifulSoup(webpage)

    text = soup.get_text().lower().replace('-',' ').replace(',',' ').replace('.',' ').replace('\n',' ').split()
    if 'covid' in text:
        covid.append(curr_url)

    for tag in soup.find_all('a', href = True):
        childUrl = tag['href']
        childUrl = urllib.parse.urljoin(seed_url, childUrl)
        if real_url in childUrl and childUrl not in seen:
            urls.append(childUrl)
            seen.append(childUrl)

print("num. of URLs seen = %d, and scanned = %d" % (len(seen), len(opened)))
print(f'num. of URLs contain covid = {len(covid)}')

print("List of covid URLs:")
for covid_url in covid:
    print(covid_url)