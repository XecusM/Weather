import requests
from bs4 import BeautifulSoup as soup
import time

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
    print('Countries Page has scrapped successfully')
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

    print('Cities Page has scrapped successfully')
    return cities

def City(city):
    weather = {'names':list(),'days':list(),'temperatures':{'time':tuple(),'temp':list(tuple())}}

    url = requests.get(city['link'])
    page = soup(url.content, 'html.parser')

    names = page.findAll('span',{'class':'b-forecast__table-days-name'})
    days = page.findAll('span',{'class':'b-forecast__table-days-date'})
    times = page.findAll('span',{'class':'b-forecast__table-value'})
    temps = page.findAll('span',{'class':'temp b-forecast__table-value'})

    print('names : {0}'.format(len(names)))
    print('days : {0}'.format(len(days)))
    print('times : {0}'.format(len(times)))
    print('temps : {0}'.format(len(temps)))


def main():
    countries = Countries()
    country = {'country':countries['country'][0],'link':countries['link'][0]}
    time.sleep(5)
    cities = Cities(country)
    city = {'city':cities['city'][0],'link':cities['link'][0]}
    time.sleep(5)
    # city = {'city':'cairo','link':'https://www.weather-forecast.com/locations/Cairo/forecasts/latest'}
    weather = City(city)


if __name__ == '__main__':
    main()
