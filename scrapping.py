from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

url = uReq("https://weather.com/weather/5day/l/9fc9a1589288fa871d909d5bfcb5cbf076c34b4ad3ccad95682640f63a783389")

page_html = url.read()

url.close()

page_soup = soup(page_html,'html.parser')
print(page_soup)
