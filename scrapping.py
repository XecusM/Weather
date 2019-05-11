import requests
from bs4 import BeautifulSoup as soup

def Countries():

    try :
        url = requests.get('https://www.weather-forecast.com/countries')
    except:
        print('Error in reading page!')
        quit()

    page = soup(url.content, 'html.parser')

    containers = page.findAll('div',{'class':'mapctrytab-cont'})

    countries = {'country':list(),'link':list()}

    for con in containers:
        links = con.findAll('a')
        for link in links:
            countries['country'].append(link.text)
            countries['link'].append('https://www.weather-forecast.com'+link['href'])

    return countries

def Cities(country):
    cities = {'city':list(),'link':list()}

    url = requests.get(country['link'])

    page = soup(url.content, 'html.parser')
    section = page.findAll('section',{'class':'b-wrapper'})
    links = section[0].findAll('a')

    for link in links:
        cities['city'].append(link.text)
        cities['link'].append('https://www.weather-forecast.com'+link['href'])


    return cities

def City(city):
    weather = {'names':list(),'days':list(),'temperatures':{'time':tuple(),'temp':list(tuple())}}

    url = requests.get(city['link'])

    page = soup(url.content, 'html.parser')
    
def main():
    # countries = Countries()
    # country = {'country':countries['country'][0],'link':countries['link'][0]}
    # cities = Cities(country)
    # city = {'city':cities['city'][0],'link':cities['link'][0]}
    city = {'city':'cairo','link':'https://www.weather-forecast.com/locations/Cairo/forecasts/latest'}


if __name__ == '__main__':
    main()
